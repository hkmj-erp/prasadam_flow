import frappe


def validate_festival_conflict(doc):
    coupons = frappe.db.sql(
        f"""
                        SELECT
                            coupon_name,festival
                        FROM `tabPF Coupon Data`
                        WHERE 
                            usable_from <= '{doc.use_date}'
                            AND (
                                usable_till IS NULL 
                                OR usable_till ="" 
                                OR usable_till >= '{doc.use_date}')
                            AND slot = '{doc.slot}'
                            AND is_public = {doc.is_public}
                            AND active = 1
                        """,
        as_dict=1,
    )
    festival_slot = False
    for c in coupons:
        if c.get("festival"):
            festival_slot = True
            break
    if festival_slot and not doc.festival:
        frappe.throw("Non-Festival Coupons can't be booked/issued in Festival Slots.")
    return
