import frappe
from frappe import local


@frappe.whitelist()
def get_short_url(long_url):
    docname = None
    # exisiting = frappe.get_all(
    #     "HKM Redirect", filters={"redirect_to": long_url}, pluck="name"
    # )
    # if exisiting:
    #     docname = exisiting[0]
    # else:
    doc = frappe.get_doc({"doctype": "HKM Redirect", "redirect_to": long_url})
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    docname = doc.name
    short_url = local.request.host_url + "sl/" + docname
    return short_url
