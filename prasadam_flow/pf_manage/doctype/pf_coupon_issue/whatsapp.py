import frappe, requests,json
from frappe.utils import cstr
from frappe.utils import getdate

def send_message(coupon_doc):
    settings = frappe.get_cached_doc("WhatsApp Settings")
    url = f"{settings.url}/{settings.version}/{settings.phone_id}/messages"

    site_name = cstr(frappe.local.site)
    
    qr_link = f"""https://{site_name}/api/method/prasadam_flow.pf_manage.doctype.pf_coupon_issue.pf_coupon_issue.get_coupon_qr?id={coupon_doc.name}"""

    payload = json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": f"+91{coupon_doc.receiver_mobile}",
    "type": "template",
    "template": {
        "name": "prasadam_coupon_2",
        "language": {
        "code": "en"
        },
        "components": [
        {
            "type": "header",
            "parameters": [
            {
                "type": "image",
                "image": {
                "link": qr_link
                }
            }
            ]
        },
        {
            "type": "body",
            "parameters": [
            {
                "type": "text",
                "text": getdate(coupon_doc.use_date).strftime("%d %B, %Y")
            },
            {
                "type": "text",
                "text": coupon_doc.slot
            },
            {
                "type": "text",
                "text": coupon_doc.number
            },
            {
                "type": "text",
                "text": coupon_doc.venue
            }
            ]
        }
        ]
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {settings.get_password("token")}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)