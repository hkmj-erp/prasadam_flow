from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        "heatmap": False,
        "fieldname": "custodian",
        "transactions": [
            {
                "label": _("Operations"),
                "items": ["PF Coupon Book", "PF Coupon Issue", "PF Issue Window"],
            },
        ],
    }
