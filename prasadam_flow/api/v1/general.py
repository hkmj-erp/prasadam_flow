import frappe
from frappe.utils import getdate
from datetime import datetime, timedelta


@frappe.whitelist()
def get_coupons_for_booking(use_date):
    from prasadam_flow.controllers.credits import get_coupons

    return get_coupons(use_date)


@frappe.whitelist()
def custodian_available_coupons(custodian, use_date):
    from prasadam_flow.controllers.credits import get_custodian_credits

    coupons_map = get_custodian_credits(custodian, use_date)
    only_coupons_with_balance = {
        k: v for k, v in coupons_map.items() if v["balance"] > 0
    }
    return list(only_coupons_with_balance.values())


@frappe.whitelist()
def custodian_available_emergency_coupons(custodian, use_date):
    from prasadam_flow.controllers.emergency import get_custodian_emergency_credits

    coupons_map = get_custodian_emergency_credits(custodian, use_date)
    only_coupons_with_balance = {
        k: v for k, v in coupons_map.items() if v["balance"] > 0
    }
    return list(only_coupons_with_balance.values())


@frappe.whitelist()
def single_coupon_availibility(coupon_data, use_date):
    from prasadam_flow.controllers.credits import get_credits_for_all_custodians

    custodians_map = get_credits_for_all_custodians(coupon_data, use_date)

    only_custodians_with_balance = {
        k: v for k, v in custodians_map.items() if v["balance"] > 0
    }
    return list(only_custodians_with_balance.values())


@frappe.whitelist()
def get_custodian_stats_day(custodian, use_date):
    from prasadam_flow.controllers.constraints import get_custodian_group_constraints

    custodian_group = frappe.db.get_value("PF Custodian", custodian, "group")
    constraints_map = get_custodian_group_constraints(custodian_group)
    use_month = getdate(use_date).strftime("%B")
    allowed = constraints_map[use_month]

    from prasadam_flow.controllers.credits import get_custodian_credits

    coupons_map = get_custodian_credits(custodian, use_date)

    for value in coupons_map.values():
        value["allowed"] = allowed[value["category"]]

    only_coupons_map_with_data = {
        k: v
        for k, v in coupons_map.items()
        if (
            v["balance"] > 0
            or v["booked"] > 0
            or v["issued"] > 0
            or v["issued_emergency"] > 0
            or v["received"] > 0
        )
    }

    coupons_data = list(only_coupons_map_with_data.values())
    return sorted(coupons_data, key=lambda x: x["balance"], reverse=True)


@frappe.whitelist(allow_guest=True)
def get_public_coupons(use_date):
    return frappe.db.sql(
        f"""
            SELECT name, slot, venue, festival, price, serving_time,booking_threshold
            FROM `tabPF Coupon Data` 
            WHERE  NOW() <= DATE_ADD(CONCAT('{use_date}', ' ', serving_time), INTERVAL -booking_threshold SECOND)
            AND active = 1 AND is_public = 1 
            AND usable_from <= '{use_date}'
            AND (usable_till IS NULL OR usable_till >= '{use_date}')
        """,
        as_dict=1,
    )
