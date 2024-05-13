from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        "heatmap": False,
        "fieldname": "group",
        "transactions": [
            {
                "label": _("Links"),
                "items": ["PF Custodian"],
            },
        ],
    }
