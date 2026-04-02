import frappe
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import cint, getdate
from frappe.model.naming import getseries


def before_naming(doc, method=None):
    if doc.get("amended_from") or doc.get("name"):
        return

    naming_series = doc.get("naming_series")
    if not naming_series:
        return

    # Resolve date
    date = (
        doc.get("posting_date")
        or getdate()
    )
    d = getdate(date)

    # Stamp fiscal fields
    try:
        fiscal_year = get_fiscal_year(date)[0]
        doc.fiscal_year = fiscal_year
        doc.fiscal = _get_fiscal(date)
    except Exception:
        pass

    if "{FY}" in naming_series or ".MM." in naming_series:
        fiscal     = _get_fiscal(date)         # "26-27"
        month_abbr = d.strftime("%b").upper()  # "APR"

        # Resolve tokens but KEEP .#### so Frappe handles the counter
        resolved = (
            naming_series
            .replace("{FY}", fiscal)
            .replace(".MM.", month_abbr)
        )
        # resolved = "26-27/APR/.####"
        # Overwrite naming_series on the doc — Frappe's autoname reads this
        doc.naming_series = resolved

        # Seed counter if series_value provided
        if cint(doc.get("series_value", 0)) > 0:
            series_key = resolved.replace(".####", "")
            _seed_series(series_key, cint(doc.series_value))


def _get_fiscal(date):
    d = getdate(date)
    if d.month >= 4:
        return f"{str(d.year)[-2:]}-{str(d.year + 1)[-2:]}"
    else:
        return f"{str(d.year - 1)[-2:]}-{str(d.year)[-2:]}"


def _seed_series(series_key, series_value):
    current = frappe.db.get_value("Series", series_key, "current", order_by="name")

    if current is None:
        frappe.db.sql(
            "INSERT INTO `tabSeries` (name, current) VALUES (%s, %s)",
            (series_key, 0)
        )

    if current != 0 or series_value > 1:
        frappe.db.sql(
            "UPDATE `tabSeries` SET current = %s WHERE name = %s",
            (series_value - 1, series_key)
        )
