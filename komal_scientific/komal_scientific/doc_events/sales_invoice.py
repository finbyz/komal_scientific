from frappe.utils import nowdate, now_datetime
from erpnext.accounts.utils import get_fiscal_year
from frappe.model.naming import NamingSeries, make_autoname

def before_naming(self, method):
    if self.get("name"):
        return

    date = self.get("posting_date") or nowdate()
    fy = get_fiscal_year(date, company=self.company)[0]
    start, end = fy.split("-")
    formatted_fy = f"{start[-2:]}-{end[-2:]}"

    month = getdate(date).strftime("%b").upper()
    self.naming_series = f"{formatted_fy}/{month}/"


def autoname(self, method):
    print("autoname called")
    fy = get_fiscal_year(nowdate(), company=self.company)[0]
    start, end = fy.split("-")
    formatted_fy = f"{start[-2:]}-{end[-2:]}"

    month = now_datetime().strftime("%b").upper()

    self.name = make_autoname(f"{formatted_fy}/{month}/.####")