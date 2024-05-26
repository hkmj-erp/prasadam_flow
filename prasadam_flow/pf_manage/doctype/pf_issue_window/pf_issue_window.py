# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from prasadam_flow.api.v1.window import encode_window_id
from prasadam_flow.api.v1.utils import get_short_url
from prasadam_flow.pf_manage.doctype.pf_coupon_issue.qr_code import get_qrcode

# from frappe.utils import get_site_name
from frappe import local


class PFIssueWindow(Document):
    @property
    def total_issued(self):
        return frappe.db.sql(
            f"SELECT SUM(number) FROM `tabPF Coupon Issue` WHERE issue_window = '{self.name}' AND docstatus = 1"
        )[0][0]


@frappe.whitelist()
def get_window_qr(data, only_qr=True):
    logo = frappe.db.get_single_value("PF Manage Settings", "qr_logo")

    if not only_qr:
        # site_name = get_site_name(frappe.local.request.host)
        window_link = (
            f"{local.request.host_url}prasadam_spw/window/{encode_window_id(data)}"
        )
        data = get_short_url(window_link)

    filedata = get_qrcode(data, logo)
    frappe.local.response.filename = f"window_{data}.png"
    frappe.local.response.filecontent = filedata.read()
    frappe.local.response.type = "download"
