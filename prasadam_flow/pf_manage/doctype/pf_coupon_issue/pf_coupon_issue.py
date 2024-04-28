# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

from prasadam_flow.pf_manage.doctype.pf_coupon_issue.qr_code import get_qrcode
from prasadam_flow.pf_manage.doctype.pf_coupon_issue.whatsapp import send_message
import frappe
from frappe.model.document import Document
from prasadam_flow.controllers.credits import get_custodian_coupon_credits
from prasadam_flow.controllers.emergency import get_custodian_emergency_coupon_credits
from prasadam_flow.controllers.thresholds import is_issue_cancel_allowed
import re


class PFCouponIssue(Document):
    def before_cancel(self):
        if self.used > 0:
            frappe.throw("Already Used (Partial or Full) Coupon can't be cancelled.")

        if not is_issue_cancel_allowed(self.coupon_data, self.use_date):
            frappe.throw("Cancellation is not allowed due to date & time thresholds.")

    def on_submit(self):
        if self.receiver_mobile:
            send_message(self)

    def before_update_after_submit(self):
        if self.number < self.used:
            frappe.throw("Used Count can't be more than the Coupon Credits.")
        return

    def before_submit(self):
        if self.receiver_mobile:
            self.receiver_mobile = re.sub(r"\D", "", self.receiver_mobile)[-10:]

    def validate(self):
        self.validate_coupon_availability()
        return

    def validate_coupon_availability(self):
        avl_credits = 0
        if self.emergency:
            avl_credits = get_custodian_emergency_coupon_credits(
                self.custodian, self.coupon_data, self.use_date
            )
        else:
            avl_credits = get_custodian_coupon_credits(
                self.custodian, self.coupon_data, self.use_date
            )
        if avl_credits < self.number:
            if self.emergency:
                frappe.throw(
                    f"Emergency Quota is not suficient to meet this requirement. Balance : {avl_credits}"
                )
            else:
                frappe.throw(
                    f"You don't have sufficent balance of coupons to Issue. Balance : {avl_credits}"
                )
        return


@frappe.whitelist(allow_guest=True)
def get_coupon_qr(id):
    logo = frappe.db.get_single_value("PF Manage Settings", "qr_logo")
    filedata = get_qrcode(id, logo)
    frappe.local.response.filename = f"cpn_{id}.png"
    frappe.local.response.filecontent = filedata.read()
    frappe.local.response.type = "download"
