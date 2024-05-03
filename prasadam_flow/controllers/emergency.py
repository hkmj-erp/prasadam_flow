import frappe
from .thresholds import is_emergency_issue_allowed


def get_custodian_emergency_coupon_credits(custodian, coupon_data, use_date):
    ## Both Pool Quota & Indivisual Quotas are needed to compare with already issued.
    emergency_pool = emergency_quota = 0
    custodian_group = frappe.get_value("PF Custodian", custodian, "group")
    emergency_use_allowed = frappe.get_value(
        "PF Coupon Data", coupon_data, "emergency_use_allowed"
    )
    if not emergency_use_allowed:
        frappe.throw("This coupon is not allowed for Emergency Use.")
    emergency_constraint_doc = frappe.get_cached_doc(
        "PF Emergency Constraint", custodian_group
    )
    for c in emergency_constraint_doc.constraints:
        if c.coupon_data == coupon_data:
            emergency_quota = c.credits
            break

    emergency_constraint_pool = frappe.get_cached_doc("PF Emergency Pool")
    for c in emergency_constraint_pool.pool:
        if c.coupon_data == coupon_data:
            emergency_pool = c.credits
            break

    total_emergency_credits_issued = 0
    custodian_emergency_credits_issued = 0
    for c in frappe.db.sql(
        f""" 
            SELECT custodian, SUM(number) as credits
            FROM `tabPF Coupon Issue`
            WHERE docstatus = 1 and coupon_data = '{coupon_data}' and use_date = '{use_date}' and emergency = 1 
            GROUP BY custodian
            """,
        as_dict=1,
    ):
        total_emergency_credits_issued += c["credits"]
        if c["custodian"] == custodian:
            custodian_emergency_credits_issued = c["credits"]

    custodian_avl_quota = emergency_quota - custodian_emergency_credits_issued

    pool_avl_quota = emergency_pool - total_emergency_credits_issued

    return min(pool_avl_quota, custodian_avl_quota)


def get_custodian_emergency_credits(custodian, use_date):
    coupons_map = {}
    for c in frappe.get_all(
        "PF Coupon Data",
        fields=["*"],
        filters={"active": 1, "is_public": 0, "emergency_use_allowed": 1},
    ):
        if is_emergency_issue_allowed(c["name"], use_date):
            coupons_map.setdefault(
                c["name"],
                {
                    **c,
                    **{
                        "balance": get_custodian_emergency_coupon_credits(
                            custodian, c["name"], use_date
                        )
                    },
                },
            )
    return coupons_map
