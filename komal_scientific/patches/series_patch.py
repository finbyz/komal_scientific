import frappe

def execute():
    # Step 1: Find highest series number from actual Sales Invoice records
    all_invoices = frappe.db.sql("""
        SELECT name FROM `tabSales Invoice`
        WHERE name REGEXP '^[0-9]{2}-[0-9]{2}/[A-Z]{3}/[0-9]+$'
    """, as_dict=True)

    fy_max = {}

    for inv in all_invoices:
        parts = inv['name'].split("/")  # ['26-27', 'APR', '0018']
        if len(parts) != 3:
            continue
        fy_key = parts[0] + "/"         # '26-27/'
        try:
            num = int(parts[2])         
        except ValueError:
            continue

        if fy_key not in fy_max:
            fy_max[fy_key] = 0
        fy_max[fy_key] = max(fy_max[fy_key], num)

    # Step 2: Update tabSeries with the actual highest number
    for fy_key, max_current in fy_max.items():
        exists = frappe.db.sql(
            f"SELECT current FROM `tabSeries` WHERE name = '{fy_key}'"
        )
        if exists:
            frappe.db.sql(
                f"UPDATE `tabSeries` SET current = {max_current} WHERE name = '{fy_key}'"
            )
        else:
            frappe.db.sql(
                f"INSERT INTO `tabSeries` (name, current) VALUES ('{fy_key}', {max_current})"
            )

        print(f"Set {fy_key} → {max_current}")

    frappe.db.commit()
    print("Migration done.")