import frappe
from frappe import local


@frappe.whitelist()
def get_short_url(long_url):
    doc = frappe.get_doc({"doctype": "HKM Redirect", "redirect_to": long_url})
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    short_url = local.request.host_url + "sl/" + doc.name
    return short_url
