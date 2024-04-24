import frappe

CUSTODIAN_ROLE = "PF Custodian"


def on_update(self, method):
    if CUSTODIAN_ROLE in frappe.get_roles():
        if not frappe.db.exists("PF Custodian", self.name):
            doc = frappe.get_doc(
                {
                    "doctype": "PF Custodian",
                    "user": self.name,
                    "group": frappe.db.get_single_value(
                        "PF Manage Settings", "general_custodian_group"
                    ),
                }
            )
            doc.insert()
