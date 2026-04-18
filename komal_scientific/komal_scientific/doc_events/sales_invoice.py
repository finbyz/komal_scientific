from frappe.utils import nowdate, now_datetime,getdate
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
    date = self.get("posting_date") or nowdate()

    fy = get_fiscal_year(date, company=self.company)[0]
    start, end = fy.split("-")
    formatted_fy = f"{start[-2:]}-{end[-2:]}"
    
    # Return / Credit Note
    if self.is_return:
        self.naming_series = f"CN/{formatted_fy}/.####"
        self.name = make_autoname(self.naming_series)
        return

    month = getdate(date).strftime("%b").upper()

    # Counter keyed to FY only (e.g. "26-27/")
    series_number = make_autoname(f"{formatted_fy}/.####")

    # Extract numeric part
    numeric_part = series_number.split("/")[-1]  # e.g. 0022

    # Final name with month injected visually
    self.name = f"{formatted_fy}/{month}/{numeric_part}"  # 26-27/MAY/0022
