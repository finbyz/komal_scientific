// Copyright (c) 2026, Mukesh and contributors
// For license information, please see license.txt

frappe.query_reports["General Ledger - Columnar"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1,
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
		},
		{
			"fieldname": "voucher_type",
			"label": __("Voucher Type"),
			"fieldtype": "Link",
			"options": "DocType",
			"get_query": function () {
				return {
					filters: {
						is_submittable: 1,
						istable: 0,
					},
				};
			},
			"on_change": function () {
				frappe.query_report.set_filter_value("voucher_no", "");
			},
		},
		{
			"fieldname": "voucher_no",
			"label": __("Voucher No"),
			"fieldtype": "Dynamic Link",
			"get_options": function () {
				let voucher_type = frappe.query_report.get_filter_value("voucher_type");
				let voucher_no = frappe.query_report.get_filter_value("voucher_no");
				if (voucher_no && !voucher_type) {
					frappe.throw(__("Please select Voucher Type first"));
				}
				return voucher_type;
			},
		},
		{
			"fieldname": "party_type",
			"label": __("Party Type"),
			"fieldtype": "Link",
			"options": "DocType",
			"get_query": function () {
				return {
					filters: {
						name: ["in", Object.keys(frappe.boot.party_account_types || {})],
					},
				};
			},
			"on_change": function () {
				frappe.query_report.set_filter_value("party", "");
			},
		},
		{
			"fieldname": "party",
			"label": __("Party"),
			"fieldtype": "Dynamic Link",
			"get_options": function () {
				return frappe.query_report.get_filter_value("party_type");
			},
		},
		{
			"fieldname": "account",
			"label": __("Account"),
			"fieldtype": "MultiSelectList",
			"get_data": function (txt) {
				return frappe.db.get_link_options("Account", txt, {
					company: frappe.query_report.get_filter_value("company"),
				});
			},
		},
	],

	onload: function (report) {
		report.page.add_inner_button(__("General Ledger"), function () {
			let filters = report.get_values() || {};
			

			frappe.set_route("query-report", "General Ledger", {
				company: filters.company,
				from_date: filters.from_date,
				to_date: filters.to_date,
				account: filters.account,
				
			});
		});

		if (!frappe.route_options) {
			report.set_filter_value({
				voucher_type: "",
				voucher_no: "",
				party_type: "",
				party: "",
			});
		}
	},

	formatter: function (value, row, column, data, default_formatter) {
		if (column.fieldtype === "Currency" && data) {
			const raw_value = data[column.fieldname];
			if (raw_value > 0) {
				// Debit Amount: Red
				const formatted_val = default_formatter(value, row, column, data);
				return `<span style="color: #e02424; font-weight: 500;">${formatted_val}</span>`;
			} else if (raw_value < 0) {
				// Credit Amount: Green (without minus sign)
				const abs_val = Math.abs(raw_value);
				const formatted_val = default_formatter(abs_val, row, column, data);
				return `<span style="color: #057a55; font-weight: 500;">${formatted_val}</span>`;
			}
		}

		return default_formatter(value, row, column, data);
	},
};


