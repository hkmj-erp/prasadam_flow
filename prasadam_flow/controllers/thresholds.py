import frappe
from datetime import datetime, timedelta
from frappe.utils import getdate


def is_issue_cancel_allowed(coupon_data, use_date):
    coupon_data_doc = frappe.get_cached_doc("PF Coupon Data", coupon_data)
    use_date = getdate(use_date)
    use_dt = (
        datetime.combine(use_date, datetime.min.time()) + coupon_data_doc.serving_time
    )
    threshold_dt = use_dt + timedelta(hours=2)
    current_datetime = datetime.now()
    return not (current_datetime > threshold_dt)


def is_emergency_issue_allowed(coupon_data, use_date):
    coupon_data_doc = frappe.get_cached_doc("PF Coupon Data", coupon_data)
    use_date = getdate(use_date)
    use_dt = (
        datetime.combine(use_date, datetime.min.time()) + coupon_data_doc.serving_time
    )

    usable_from = use_dt - timedelta(hours=2)
    usable_till = use_dt + timedelta(hours=3)

    # threshold_dt = use_dt + timedelta(
    #     hours=3
    # )  ## Till 3 hours post Serving Time, Emergency Coupons can be issued.

    current_datetime = datetime.now()
    return usable_till >= current_datetime >= usable_from


def is_booking_allowed(coupon_data, use_date):
    coupon_data_doc = frappe.get_cached_doc("PF Coupon Data", coupon_data)
    use_date = getdate(use_date)

    if (use_date < coupon_data_doc.usable_from) or (
        (coupon_data_doc.usable_till is not None)
        and (use_date > coupon_data_doc.usable_till)
    ):
        return False
    use_dt = (
        datetime.combine(use_date, datetime.min.time()) + coupon_data_doc.serving_time
    )
    threshold_dt = use_dt - timedelta(seconds=coupon_data_doc.booking_threshold)
    current_datetime = datetime.now()
    return not (current_datetime > threshold_dt)


def is_transfer_allowed(coupon_data, use_date):
    coupon_data_doc = frappe.get_cached_doc("PF Coupon Data", coupon_data)

    if not coupon_data_doc.transferable:
        return False

    if not coupon_data_doc.transfer_threshold:
        return True

    use_date = getdate(use_date)

    use_dt = (
        datetime.combine(use_date, datetime.min.time()) + coupon_data_doc.serving_time
    )

    threshold_dt = use_dt + timedelta(seconds=coupon_data_doc.transfer_threshold)
    current_datetime = datetime.now()
    return not (current_datetime > threshold_dt)


def is_cancel_allowed(coupon_data, use_date):
    coupon_data_doc = frappe.get_cached_doc("PF Coupon Data", coupon_data)

    use_date = getdate(use_date)

    use_dt = (
        datetime.combine(use_date, datetime.min.time()) + coupon_data_doc.serving_time
    )

    threshold_dt = use_dt - timedelta(seconds=coupon_data_doc.cancel_threshold)
    current_datetime = datetime.now()

    return not (current_datetime > threshold_dt)
