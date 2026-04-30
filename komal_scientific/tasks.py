import frappe
from frappe.utils import cint, today
from frappe.email.doctype.notification.notification import get_emails_from_template

def _get_settings():
    """Load Payment Reminder Settings and return as a dict."""
    return frappe.db.get_singles_dict("Payment Reminder Settings")


def send_payment_reminders():
    """
    Fetch all submitted Sales Invoices that are Overdue / Partly Paid / Unpaid
    and whose due_date has passed. Send a reminder email for each, respecting:
      - Global kill-switch  : Payment Reminder Settings.enable_payment_reminders
      - Per-customer disable: Customer.disable_payment_reminders (Check field)
      - Per-invoice disable : Sales Invoice.disable_payment_reminder (Check field)

    Email configuration (From, CC, Subject, Body) is managed entirely inside
    the  Payment Reminder Settings  single DocType — mirroring Notification behavior.
    """

    cfg = _get_settings()

    #  Global Kill-Switch
    if not cint(cfg.get("enable_payment_reminders")):
        return

    #  Read config from Settings DocType 
    email_account = cfg.get("from_email")
    if not email_account:
        return
    from_email = frappe.get_value("Email Account", email_account, "email_id")
    if not from_email:
        return

    recipient_field = cfg.get("recipient_field") or "contact_email"
    cc_template = cfg.get("cc_emails") or ""
    subject_template = cfg.get("email_subject") or ""
    body_template = cfg.get("email_body") or ""

    if not subject_template or not body_template:
        return

    #  Fetch overdue invoices
    invoices = frappe.get_all(
        "Sales Invoice",
        filters={
            "docstatus": 1,
            "status": ["in", ["Overdue", "Partly Paid"]],
            "due_date": ["<", today()],
            "disable_payment_reminder": 0,
        },
        fields=["name", "customer", "last_reminder_sent"]
    )



    today_str = today()
    is_monday = frappe.utils.getdate().weekday() == 0

    for inv_summary in invoices:
        #  Monday / First-time check
        # Logic: Send if (never sent before) OR (today is Monday and not sent today)
        last_sent = inv_summary.get("last_reminder_sent")
        
        should_send = False
        if not last_sent:
            should_send = True
        elif is_monday and str(last_sent) != today_str:
            should_send = True
            
        if not should_send:
            continue

        try:
            invoice_doc = frappe.get_doc("Sales Invoice", inv_summary["name"])
            ctx = {"doc": invoice_doc}

            #  Per-customer disable check
            customer_disabled = frappe.db.get_value(
                "Customer", invoice_doc.customer, "disable_payment_reminders"
            )
            if cint(customer_disabled):
                continue

            # Resolve recipients 
            # Ensure recipients and cc_list are lists for proper truthiness check 
            # and sendmail compatibility.
            recipients = invoice_doc.get(recipient_field)
            if recipients:
                recipients = [email.strip() for email in recipients.split(",") if email.strip()]
            
            if not recipients:
                continue

            cc_list =  cc_template if cc_template else ""
            if cc_list:
                cc_list = [email.strip() for email in cc_list.split(",") if email.strip()]
            #  Render subject & body 
            subject = frappe.render_template(subject_template, ctx)
            message = frappe.render_template(body_template, ctx)

            #  Send email
            frappe.sendmail(
                recipients=recipients,
                sender=from_email,
                cc=cc_list,
                subject=subject,
                message=message,
                reference_doctype="Sales Invoice",
                reference_name=invoice_doc.name,
            )

            #  Stamp last reminder date on the invoice
            frappe.db.set_value(
                "Sales Invoice",
                invoice_doc.name,
                "last_reminder_sent",
                today(),
                update_modified=False,
            )

        except Exception:
            frappe.log_error(title=f"Payment Reminder Error: {inv_summary['name']}",message = frappe.get_traceback())
            continue
