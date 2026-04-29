# Copyright (c) 2026, Komal Scientific and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PaymentReminderSettings(Document):
	def validate(self):
		self.validate_recipient_field()

	def validate_recipient_field(self):
		if not self.recipient_field:
			return

		self.recipient_field = self.recipient_field.strip()
		if not frappe.get_meta("Sales Invoice").has_field(self.recipient_field):
			frappe.throw(
				f"Recipient Field must be a valid Sales Invoice fieldname. "
				f"Field not found: {self.recipient_field}"
			)
