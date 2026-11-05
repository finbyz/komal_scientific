# Copyright (c) 2026, Mukesh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_columns(filters)
	data, totals = get_data(filters, columns)
	chart = get_chart_data(columns, totals, filters)
	report_summary = get_report_summary(totals, data, filters)

	return columns, data, None, chart, report_summary


def get_columns(filters):
	# Base columns
	columns = [
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 110,
		},
		{
			"label": _("Voucher Type"),
			"fieldname": "voucher_type",
			"fieldtype": "Link",
			"options": "DocType",
			"width": 140,
		},
		{
			"label": _("Voucher No"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 160,
		},
		{
			"label": _("Party Type"),
			"fieldname": "party_type",
			"fieldtype": "Link",
			"options": "DocType",
			"width": 110,
		},
		{
			"label": _("Party"),
			"fieldname": "party",
			"fieldtype": "Dynamic Link",
			"options": "party_type",
			"width": 160,
		},
	]

	# Dynamic account columns will be added in get_data
	return columns


def get_data(filters, columns):
	voucher_conditions, party_conditions, account_conditions = get_conditions(filters)

	base_where = "is_cancelled = 0"
	if voucher_conditions:
		base_where += " AND " + " AND ".join(voucher_conditions)

	joins = []
	gle_voucher_conditions = ["gle." + c for c in voucher_conditions] if voucher_conditions else []
	gle_where = "gle.is_cancelled = 0"
	if gle_voucher_conditions:
		gle_where += " AND " + " AND ".join(gle_voucher_conditions)

	if account_conditions:
		acc_where = base_where + " AND " + " AND ".join(account_conditions)
		joins.append(
			f"""
			INNER JOIN (
				SELECT DISTINCT voucher_type, voucher_no
				FROM `tabGL Entry`
				WHERE {acc_where}
			) matched_acc
				ON gle.voucher_type = matched_acc.voucher_type
				AND gle.voucher_no = matched_acc.voucher_no
			"""
		)

	if party_conditions:
		party_where = base_where + " AND " + " AND ".join(party_conditions)
		joins.append(
			f"""
			INNER JOIN (
				SELECT DISTINCT voucher_type, voucher_no
				FROM `tabGL Entry`
				WHERE {party_where}
			) matched_party
				ON gle.voucher_type = matched_party.voucher_type
				AND gle.voucher_no = matched_party.voucher_no
			"""
		)

	if joins:
		joins_str = "\n".join(joins)
		query = f"""
			SELECT
				gle.name,
				gle.posting_date,
				gle.voucher_type,
				gle.voucher_no,
				gle.party_type,
				gle.party,
				gle.account,
				gle.debit,
				gle.credit
			FROM
				`tabGL Entry` gle
			{joins_str}
			WHERE
				{gle_where}
			ORDER BY
				gle.posting_date ASC, gle.voucher_type ASC, gle.voucher_no ASC, gle.creation ASC
		"""
	else:
		query = f"""
			SELECT
				name,
				posting_date,
				voucher_type,
				voucher_no,
				party_type,
				party,
				account,
				debit,
				credit
			FROM
				`tabGL Entry`
			WHERE
				{base_where}
			ORDER BY
				posting_date ASC, voucher_type ASC, voucher_no ASC, creation ASC
		"""

	gl_entries = frappe.db.sql(query, filters, as_dict=1)

	totals = {
		"total_debit": 0.0,
		"total_credit": 0.0,
		"account_totals": {},
	}

	if not gl_entries:
		return [], totals

	# Get all unique accounts from the entries
	unique_accounts = []
	seen_accounts = set()
	for entry in gl_entries:
		totals["total_debit"] += flt(entry.debit)
		totals["total_credit"] += flt(entry.credit)
		if entry.account:
			totals["account_totals"][entry.account] = totals["account_totals"].get(entry.account, 0.0) + (
				flt(entry.debit) - flt(entry.credit)
			)
			if entry.account not in seen_accounts:
				seen_accounts.add(entry.account)
				unique_accounts.append(entry.account)
    
    

	# Sort accounts for consistent column ordering
	unique_accounts.sort()

	# Map account to safe fieldname
	account_field_map = {}
	company_currency = None
	if filters.get("company"):
		company_currency = frappe.get_cached_value("Company", filters.get("company"), "default_currency")

	for acc in unique_accounts:
		field_name = frappe.scrub(acc)
		account_field_map[acc] = field_name
		columns.append(
			{
				"label": _(acc),
				"fieldname": field_name,
				"fieldtype": "Currency",
				"options": "currency" if not company_currency else None,
				"width": 140,
			}
		)

	# Group entries by (posting_date, voucher_type, voucher_no)
	data_map = {}
	for entry in gl_entries:
		key = (entry.posting_date, entry.voucher_type, entry.voucher_no)
		if key not in data_map:
			data_map[key] = {
				"posting_date": entry.posting_date,
				"voucher_type": entry.voucher_type,
				"voucher_no": entry.voucher_no,
				"party_type": entry.party_type or "",
				"party": entry.party or "",
				"currency": company_currency,
			}
			# Initialise every dynamic account column to 0 so inline filters work
			for field_name in account_field_map.values():
				data_map[key][field_name] = 0.0	
		else:
			# If party wasn't set earlier on the voucher row, set it
			if not data_map[key].get("party") and entry.party:
				data_map[key]["party_type"] = entry.party_type or ""
				data_map[key]["party"] = entry.party or ""
			elif entry.party and entry.party not in data_map[key]["party"]:
				data_map[key]["party"] += f", {entry.party}"

		acc_field = account_field_map.get(entry.account)
		if acc_field:
			# Debit value as positive, Credit value as negative (-credit)
			val = flt(entry.debit) - flt(entry.credit)
			data_map[key][acc_field] = flt(data_map[key].get(acc_field, 0.0)) + val

	data = list(data_map.values())
	return data, totals


def get_report_summary(totals, data, filters):
	company_currency = None
	if filters.get("company"):
		company_currency = frappe.get_cached_value("Company", filters.get("company"), "default_currency")

	total_debit = flt(totals.get("total_debit", 0.0))
	total_credit = flt(totals.get("total_credit", 0.0))
	voucher_count = len(data)

	return [
		{
			"value": total_debit,
			"label": _("Total Debit"),
			"datatype": "Currency",
			"currency": company_currency,
			"indicator": "Red",
		},
		{
			"value": total_credit,
			"label": _("Total Credit"),
			"datatype": "Currency",
			"currency": company_currency,
			"indicator": "Green",
		},
		{
			"value": voucher_count,
			"label": _("Total Transactions"),
			"datatype": "Int",
			"indicator": "Blue",
		},
	]


def get_chart_data(columns, totals, filters):
	account_totals = totals.get("account_totals", {})
	if not account_totals:
		return None

	# Top 10 accounts by volume
	sorted_accounts = sorted(
		account_totals.items(), key=lambda x: abs(x[1]), reverse=True
	)[:10]

	labels = [acc[0] for acc in sorted_accounts]
	values = [acc[1] for acc in sorted_accounts]

	return {
		"data": {
			"labels": labels,
			"datasets": [
				{
					"name": _("Net Balance"),
					"values": values,
				}
			],
		},
		"type": "bar",
		"colors": ["#5e64ff"],
	}


def get_conditions(filters):
	voucher_conditions = []
	party_conditions = []
	account_conditions = []

	if filters.get("company"):
		voucher_conditions.append("company = %(company)s")

	if filters.get("from_date"):
		voucher_conditions.append("posting_date >= %(from_date)s")

	if filters.get("to_date"):
		voucher_conditions.append("posting_date <= %(to_date)s")

	if filters.get("voucher_type"):
		voucher_conditions.append("voucher_type = %(voucher_type)s")

	if filters.get("voucher_no"):
		voucher_conditions.append("voucher_no = %(voucher_no)s")

	if filters.get("party_type"):
		party_conditions.append("party_type = %(party_type)s")

	if filters.get("party"):
		party = filters.get("party")
		if isinstance(party, str) and party.startswith("[") and party.endswith("]"):
			try:
				party = frappe.parse_json(party)
				filters["party"] = party
			except Exception:
				pass
		if isinstance(party, (list, tuple)):
			if party:
				party_conditions.append("party IN %(party)s")
		elif party:
			party_conditions.append("party = %(party)s")

	if filters.get("account"):
		acc = filters.get("account")
		if isinstance(acc, str) and acc.startswith("[") and acc.endswith("]"):
			try:
				acc = frappe.parse_json(acc)
				filters["account"] = acc
			except Exception:
				pass
		if isinstance(acc, (list, tuple)):
			if acc:
				account_conditions.append("account IN %(account)s")
		elif acc:
			account_conditions.append("account = %(account)s")

	return voucher_conditions, party_conditions, account_conditions

