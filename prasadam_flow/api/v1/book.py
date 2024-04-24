import hashlib, requests
import frappe, base64, json
from frappe.model.docstatus import DocStatus
from frappe.utils import get_site_name
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env


fields = [
    "custodian",
    "coupon_data",
    "use_date",
    "number",
    "receiver_name",
    "receiver_mobile",
]


@frappe.whitelist(allow_guest=True, methods=["POST"])
def request(data):
    doc = frappe.get_doc({**data, "doctype": "PF Coupon Book", "is_public": 1})
    doc.insert(ignore_permissions=True)
    return get_phonepay_redirect_url(doc)


def get_phonepay_client():
    settings = frappe.get_cached_doc("PF Manage Settings")
    return PhonePePaymentClient(
        merchant_id=settings.phonepay_merchant_id,
        salt_key=settings.get_password("phonepay_salt_key"),
        salt_index=1,
        env=Env.PROD,
    )


def get_phonepay_redirect_url(booking_doc):
    unique_transaction_id = booking_doc.name
    ui_redirect_url = f"https://donation.harekrishnajaipur.org/thankyou?booking_id={booking_doc.name}"
    s2s_callback_url = f"https://{get_site_name(frappe.local.request.host)}/api/method/prasadam_flow.api.v1.book.phonepay_callback"
    # s2s_callback_url = "https://webhook.site/82e1be72-39e6-4dc4-b6cc-4f84f229b4a6"
    amount = frappe.db.get_value("PF Coupon Data", booking_doc.coupon_data, "price") * 100 * booking_doc.number
    id_assigned_to_user_by_merchant = booking_doc.receiver_mobile
    pay_page_request = PgPayRequest.pay_page_pay_request_builder(
        merchant_transaction_id=unique_transaction_id,
        amount=amount,
        merchant_user_id=id_assigned_to_user_by_merchant,
        callback_url=s2s_callback_url,
        redirect_url=ui_redirect_url,
    )
    phonepe_client = get_phonepay_client()
    pay_page_response = phonepe_client.pay(pay_page_request)
    pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
    return pay_page_url


@frappe.whitelist(allow_guest=True)
def phonepay_callback():
    incoming_payload = frappe.request.data.decode()
    incoming_headers = frappe.request.headers
    phonepe_client = get_phonepay_client()
    payload = json.loads(incoming_payload)

    is_valid = phonepe_client.verify_response(
        x_verify=incoming_headers['x-verify'],
        response=incoming_payload,
    )
    if is_valid:
        decoded_string = base64.b64decode(payload['response'])
        response = json.loads(decoded_string.decode("utf-8"))
        issue_coupon(response["data"]["merchantTransactionId"])
        return {"booking_id":response["data"]["merchantTransactionId"]}
    else:
        frappe.throw("Invalid Request.")

def issue_coupon(coupon_id):
    booking_doc = frappe.get_doc("PF Coupon Book", coupon_id)
    booking_doc.docstatus = DocStatus.submitted()
    booking_doc.save(ignore_permissions = True)
    issue_doc = frappe.get_doc({
        "doctype": "PF Coupon Issue",
        "custodian":booking_doc.custodian,
        "coupon_data":booking_doc.coupon_data,
        "use_date":booking_doc.use_date,
        "number":booking_doc.number,
        "receiver_name":booking_doc.receiver_name,
        "receiver_mobile":booking_doc.receiver_mobile,
        "connected_booking":booking_doc.name,
        "docstatus":1,
        "is_public": 1})
    issue_doc.save(ignore_permissions = True)
    frappe.db.commit()
    send_data_to_marketing_team(booking_doc)

def send_data_to_marketing_team(booking_doc):
    url = 'https://harekrishnajaipur.org/api/prasadam_booking_details'
    myobj = {
                'name': booking_doc.receiver_name,
                'mobile':booking_doc.receiver_mobile
             }
    requests.post(url, json = myobj)
    