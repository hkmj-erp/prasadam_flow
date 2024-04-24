import frappe
from datetime import datetime
from frappe.utils import getdate


def get_custodian_quota(custodian, use_date, coupon_data):
    custodian_group = frappe.db.get_value("PF Custodian", custodian, "group")
    constraints_map = get_custodian_group_constraints(custodian_group)
    use_month = getdate(use_date).strftime("%B")
    coupon_category = frappe.db.get_value("PF Coupon Data", coupon_data, "category")
    allowed = constraints_map[use_month][coupon_category]
    booked = 0
    booked_query_result = frappe.db.sql(
        f""" 
                SELECT SUM(number) 
                FROM `tabPF Coupon Book`
                WHERE docstatus = 1 and custodian = '{custodian}' and coupon_data = '{coupon_data}'"""
    )
    if booked_query_result[0][0]:
        booked = booked_query_result[0][0]
    return allowed - booked


def get_monthly_constraints(month=None):
    if month is None:
        month = datetime.now().strftime("%B")

    coupon_categories = frappe.get_all(
        "PF Coupon Category", filters={"active": 1}, pluck="name"
    )

    custodian_group_map = (
        frappe.cache().hget("pf_month_constraint", month) or frappe._dict()
    )

    if not custodian_group_map:
        ## Get Fresh Data of Constraints since not available in Cache Memory
        for cg in frappe.get_all(
            "PF Custodian Group", filters={"active": 1}, pluck="name"
        ):
            custodian_group_map.setdefault(
                cg,
                frappe._dict(
                    custodian_group=cg,
                ),
            )
            for cc in coupon_categories:
                custodian_group_map[cg][cc] = 0

        ### Traverse Monthly Constraints

        for mc in frappe.db.sql(
            f"""
					select pmc.custodian_group, pmcd.coupon_category as category, pmcd.credits
					from `tabPF Month Constraint` pmc
					join `tabPF Month Constraint Detail` pmcd
					on pmcd.parent = pmc.name
					where pmc.constraint_month = "{month}"
						""",
            as_dict=1,
        ):
            custodian_group_map[mc["custodian_group"]][mc["category"]] = mc["credits"]

        ### Traverse Regular Constraints

        for mc in frappe.db.sql(
            f"""
					select pmc.custodian_group, pmcd.coupon_category as category, pmcd.credits
					from `tabPF Month Constraint Regular` pmc
					join `tabPF Month Constraint Detail` pmcd
					on pmcd.parent = pmc.name
					where 1
						""",
            as_dict=1,
        ):
            if custodian_group_map[mc["custodian_group"]][mc["category"]] == 0:
                custodian_group_map[mc["custodian_group"]][mc["category"]] = mc[
                    "credits"
                ]
        ## Set Constraints in Cache Memory
        frappe.cache().hset("pf_month_constraint", month, custodian_group_map)

    return custodian_group_map


def get_custodian_group_constraints(custodian_group):

    coupon_categories = frappe.get_all(
        "PF Coupon Category", filters={"active": 1}, pluck="name"
    )

    months_map = (
        frappe.cache().hget("pf_month_constraint", custodian_group) or frappe._dict()
    )

    if not months_map:
        ## Get Fresh Data of Constraints since not available in Cache Memory
        import calendar

        months = list(calendar.month_name)[1:]
        for month in months:
            months_map.setdefault(
                month,
                frappe._dict(
                    month=month,
                ),
            )
            for cc in coupon_categories:
                months_map[month][cc] = 0

        ### Traverse Monthly Constraints

        for mc in frappe.db.sql(
            f"""
					select pmc.constraint_month, pmcd.coupon_category as category, pmcd.credits
					from `tabPF Month Constraint` pmc
					join `tabPF Month Constraint Detail` pmcd
					on pmcd.parent = pmc.name
					where pmc.custodian_group = "{custodian_group}"
						""",
            as_dict=1,
        ):
            months_map[mc["constraint_month"]][mc["category"]] = mc["credits"]

        ### Traverse Regular Constraints

        for rc in frappe.db.sql(
            f"""
					select pmcd.coupon_category as category, pmcd.credits
					from `tabPF Month Constraint Regular` pmc
					join `tabPF Month Constraint Detail` pmcd
					on pmcd.parent = pmc.name
					where pmc.custodian_group = '{custodian_group}'
						""",
            as_dict=1,
        ):
            for month in months:
                if months_map[month][rc["category"]] == 0:
                    months_map[month][rc["category"]] = rc["credits"]
        ## Set Constraints in Cache Memory
        frappe.cache().hset("pf_month_constraint", custodian_group, months_map)

    return months_map
