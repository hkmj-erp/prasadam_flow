from cryptography.fernet import Fernet
import frappe, re, json, string
from datetime import datetime
from hkm.mobile_app.auth import random_string_generator
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils import today
from prasadam_flow.controllers.credits import get_custodian_coupon_credits


@frappe.whitelist()
def encode_window_id(windowId):
    settings = frappe.get_cached_doc("PF Manage Settings")

    if not settings.public_fernet_key:
        key = Fernet.generate_key()
        frappe.db.set_value(
            "PF Manage Settings",
            "PF Manage Settings",
            "public_fernet_key",
            key.decode(),
        )
        frappe.db.commit()
    else:
        key = settings.public_fernet_key.encode()

    f = Fernet(key)
    token = f.encrypt(windowId.encode())
    return token.decode()


def decode_window_id(encryptedId):
    settings = frappe.get_cached_doc("PF Manage Settings")
    f = Fernet(settings.public_fernet_key.encode())
    windowId = (f.decrypt(encryptedId.encode())).decode()
    if not frappe.db.exists("PF Issue Window", windowId, cache=True):
        frappe.throw("This Window ID is invalid.")
    return windowId


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_window_details(encrypted_window_id):
    id = decode_window_id(encrypted_window_id)
    window_doc = frappe.get_doc("PF Issue Window", id)
    recent_issues = None
    credits_left = None
    if window_doc.recent_coupons_visibility:
        recent_issues = frappe.get_all(
            "PF Coupon Issue",
            filters={"issue_window": id, "docstatus": 1},
            fields=[
                "use_date",
                "number",
                "used",
                "receiver_name",
                "receiver_mobile",
                "coupon_data",
                "slot",
                "venue",
                "serving_time",
                "creation",
                "name",
            ],
            order_by="creation desc",
            page_length=500,
        )
        credits_left = get_custodian_coupon_credits(
            window_doc.custodian, window_doc.coupon_data, window_doc.use_date
        )
    response = frappe._dict(
        limit=window_doc.single_time_limit,
        credits=credits_left,
        recent_issues=recent_issues,
    )

    return response


@frappe.whitelist(allow_guest=True, methods=["POST"])
def get_coupon():
    data = json.loads(frappe.request.data)
    encrypted_window_id = data.get("encrypted_window_id")
    name = data.get("name")
    mobile = data.get("mobile")
    number = data.get("number")
    # return encrypted_window_id
    id = decode_window_id(encrypted_window_id)
    doc = frappe.get_doc("PF Issue Window", id)

    current_datetime = datetime.now()

    if not (doc.from_datetime <= current_datetime <= doc.to_datetime):
        frappe.throw("Window for Issuing coupons is closed at this time.")

    if len(name) <= 5:
        frappe.throw("Please write your full name.")

    if number > doc.single_time_limit:
        frappe.throw(f"Coupon count can not be more than {doc.single_time_limit}")

    cleaned_mobile = re.sub(r"\D", "", str(mobile))[-10:]
    if len(cleaned_mobile) != 10:
        frappe.throw("Mobile Number is not of 10 digits")

    if frappe.db.exists(
        "PF Coupon Issue",
        {"issue_window": doc.name, "receiver_mobile": cleaned_mobile, "docstatus": 1},
    ):
        frappe.throw("Coupon already issued to this Mobile Number.")

    frappe.session.user = doc.custodian
    issue_doc = frappe.get_doc(
        {
            "doctype": "PF Coupon Issue",
            "custodian": doc.custodian,
            "coupon_data": doc.coupon_data,
            "use_date": doc.use_date,
            "number": number,
            "receiver_name": name,
            "receiver_mobile": cleaned_mobile,
            "docstatus": 1,
            "issue_window": doc.name,
        }
    )
    issue_doc.save()
    return issue_doc.name


REDIS_PREFIX = "prasadam_otp"


@frappe.whitelist(allow_guest=True, methods=["POST"])
def prasadam_mobile_generate_otp():
    data = json.loads(frappe.request.data)
    mobile = data.get("mobile")
    cleaned_mobile = re.sub(r"\D", "", str(mobile))[-10:]

    key = f"{REDIS_PREFIX}:{cleaned_mobile}"
    otp = None
    if frappe.cache().get(key):
        otp = frappe.cache().get(key).decode("utf-8")
    else:
        otp = random_string_generator(6, string.digits)
        frappe.cache().set(key, otp, ex=600)

    message = f"""Your app code is: {otp} \n-Hare Krishna Movement \nApp Hash: """
    send_sms(receiver_list=[cleaned_mobile], msg=message)


@frappe.whitelist(allow_guest=True, methods=["POST"])
def prasadam_mobile_get_coupons():
    data = json.loads(frappe.request.data)
    mobile = data.get("mobile")
    otp = data.get("otp")
    use_date = data.get("use_date") or today()
    cleaned_mobile = re.sub(r"\D", "", str(mobile))[-10:]
    key = f"{REDIS_PREFIX}:{cleaned_mobile}"

    if not frappe.cache().get(key):
        frappe.throw("No OTP Sent or Expired.")

    stored_otp = frappe.cache().get(key).decode("utf-8")
    if stored_otp == otp:
        return frappe.get_all(
            "PF Coupon Issue",
            filters={
                "receiver_mobile": cleaned_mobile,
                "docstatus": 1,
                "use_date": use_date,
            },
            fields=[
                "name",
                "custodian",
                "slot",
                "venue",
                "serving_time",
                "number",
                "used",
                "coupon_data",
            ],
        )
    else:
        frappe.throw("OTP didn't match.")
