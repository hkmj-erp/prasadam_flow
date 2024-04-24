# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

CUSTODIAN_ROLE = "PF Custodian"


class PFCustodian(Document):
    def on_update(self):
        if CUSTODIAN_ROLE not in frappe.get_roles(self.user):
            user = frappe.get_doc("User", self.user)
            user.add_roles([CUSTODIAN_ROLE])
