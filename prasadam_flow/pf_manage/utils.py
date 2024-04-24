import frappe


def check(use_date, slot):
    coupons = frappe.db.sql(
        f"""
                    SELECT
                        coupon_name,festival
                    FROM `tabPF Coupon Data`
                    WHERE 
                        usable_from <= '{use_date}'
                        AND (
                            usable_till IS NULL 
                            OR usable_till ="" 
                            OR usable_till >= '{use_date}')
                        AND slot = '{slot}'
                        AND is_public = 0
                    """,
        as_dict=1,
    )

    festival_found = any(c.get("festival") is not None for c in coupons)

    print(coupons)
    print(festival_found)
