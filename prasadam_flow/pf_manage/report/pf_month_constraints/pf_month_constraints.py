# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from prasadam_flow.controllers.constraints import (
    get_monthly_constraints,
    get_custodian_group_constraints,
)


def execute(filters=None):

    if not filters:
        filters = {}

    coupon_categories = frappe.get_all(
        "PF Coupon Category", filters={"active": 1}, pluck="name"
    )

    if filters.get("wise") == "Month Wise":
        credits_map = get_monthly_constraints(month=filters.get("month"))
    else:
        credits_map = get_custodian_group_constraints(
            custodian_group=filters.get("custodian_group")
        )

    columns = get_columns(coupon_categories, filters)

    data = list(credits_map.values())

    return columns, data


def get_columns(coupon_categories, filters):
    columns = []
    if filters.get("wise") == "Month Wise":
        columns.append(
            {
                "label": "Custodian Group",
                "fieldname": "custodian_group",
                "fieldtype": "Link",
                "options": "PF Custodian Group",
                "width": 120,
            },
        )
    else:
        columns.append(
            {
                "label": "Month",
                "fieldname": "month",
                "fieldtype": "Data",
                "width": 120,
            },
        )
    for c in coupon_categories:
        columns.append(
            {
                "label": c,
                "fieldname": c,
                "fieldtype": "Int",
                "width": 120,
            }
        )
    return columns
