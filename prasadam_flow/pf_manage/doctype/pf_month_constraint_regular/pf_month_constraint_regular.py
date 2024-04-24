# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import calendar


class PFMonthConstraintRegular(Document):
    def on_update(self):
        self.delete_month_constraint_key()
        self.delete_custodian_group_constraint_key()

    def on_trash(self):
        self.delete_month_constraint_key()
        self.delete_custodian_group_constraint_key()

    def delete_month_constraint_key(self):
        months = list(calendar.month_name)[1:]
        for month in months:
            frappe.cache().hdel("pf_month_constraint", month)

    def delete_custodian_group_constraint_key(self):
        for group in frappe.get_all(
            "PF Custodian Group", filters={"active": 1}, pluck="name"
        ):
            frappe.cache().hdel("pf_month_constraint", group)
