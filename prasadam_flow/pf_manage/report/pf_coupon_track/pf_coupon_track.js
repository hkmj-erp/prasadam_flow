// Copyright (c) 2024, Narahari Dasa and contributors
// For license information, please see license.txt

frappe.query_reports["PF Coupon Track"] = {
	"filters": [
		{
			"fieldname": "use_date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": (new Date()),
			"width": 80,
		},
		{
			"fieldname": "coupon_data",
			"label": __("Coupon Data"),
			"fieldtype": "Link",
			"options": "PF Coupon Data",
			"reqd": 1,
			"width": 80,
		}
	]
};
