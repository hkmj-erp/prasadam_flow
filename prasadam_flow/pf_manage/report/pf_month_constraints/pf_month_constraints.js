// Copyright (c) 2024, Narahari Dasa and contributors
// For license information, please see license.txt

months = [
	"January",
	"February",
	"March",
	"April",
	"May",
	"June",
	"July",
	"August",
	"September",
	"October",
	"November",
	"December"]

frappe.query_reports["PF Month Constraints"] = {
	"filters": [
		{
			"fieldname": "wise",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": ["Month Wise", "Custodian Group Wise"],
			"reqd": 1,
			"width": 80,
			"default": "Month Wise",
			on_change: function () {
				let wise = frappe.query_report.get_filter_value('wise');
				console.log(wise);
				frappe.query_report.toggle_filter_display('custodian_group', wise === 'Month Wise');
				frappe.query_report.toggle_filter_display('month', wise === 'Custodian Group Wise');
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": months.join("\n"),
			"reqd": 1,
			"width": 80,
			"default": months[(new Date()).getMonth()]
		},
		{
			"fieldname": "custodian_group",
			"label": __("Custodian Group"),
			"fieldtype": "Link",
			"hidden": 1,
			"options": "PF Custodian Group",
			"width": 80
		},
	]
};
