import frappe
from datetime import datetime, timedelta, date


def execute():
    today_date = date.today()
    next_day_date = today_date + timedelta(days=1)
    next_day_weekday = next_day_date.strftime("%A")
    for custodian, coupon, credits in frappe.db.sql(
        f"""
                    SELECT
                        bs.custodian, bs.coupon, bsd.credits
                    FROM `tabPF Coupon Book Schedule` bs
                    JOIN `tabPF Coupon Book Schedule Detail` bsd
                        ON bs.name = bsd.parent AND bs.active = 1
                    WHERE
                        bsd.week_day = '{next_day_weekday}'
                    """
    ):
        doc = frappe.get_doc(
            {
                "doctype": "PF Coupon Book",
                "custodian": custodian,
                "coupon_data": coupon,
                "use_date": next_day_date,
                "number": credits,
            }
        )

        doc.insert(ignore_permissions=True)
        doc.submit()
        ## Notify Custodian
        settings_doc = frappe.get_cached_doc("PF Manage Settings")
        notif_doc = frappe.get_doc(
            {
                "doctype": "App Notification",
                "app": settings_doc.firebase_admin_app,
                "channel": settings_doc.coupon_auto_booking_channel,
                "user": custodian,
                "subject": "Auto Booked!",
                "message": f"Your coupons have auto booked as per Schedule.\nUse Date: {next_day_date}\nCoupon: {coupon}\nNumber: {credits}",
            }
        )
        notif_doc.insert(ignore_permissions=True)

    frappe.db.commit()
