# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PFIssueWindow(Document):
    @property
    def total_issued(self):
        return frappe.db.sql(
            f"SELECT SUM(number) FROM `tabPF Coupon Issue` WHERE issue_window = '{self.name}' AND docstatus = 1"
        )[0][0]
