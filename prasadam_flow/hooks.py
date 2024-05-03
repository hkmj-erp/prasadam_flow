app_name = "prasadam_flow"
app_title = "Prasadam Flow"
app_publisher = "Narahari Dasa"
app_description = "Prasadam Coupon Distribution System for HKM Center"
app_email = "nrhdasa@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/prasadam_flow/css/prasadam_flow.css"
# app_include_js = "/assets/prasadam_flow/js/prasadam_flow.js"

# include js, css files in header of web template
# web_include_css = "/assets/prasadam_flow/css/prasadam_flow.css"
# web_include_js = "/assets/prasadam_flow/js/prasadam_flow.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "prasadam_flow/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "prasadam_flow/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "prasadam_flow.utils.jinja_methods",
# 	"filters": "prasadam_flow.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "prasadam_flow.install.before_install"
# after_install = "prasadam_flow.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "prasadam_flow.uninstall.before_uninstall"
# after_uninstall = "prasadam_flow.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "prasadam_flow.utils.before_app_install"
# after_app_install = "prasadam_flow.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "prasadam_flow.utils.before_app_uninstall"
# after_app_uninstall = "prasadam_flow.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "prasadam_flow.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "PF Coupon Transfer": "prasadam_flow.pf_manage.doctype.pf_coupon_transfer.pf_coupon_transfer_filter.list_filter",
    "PF Coupon Book": "prasadam_flow.pf_manage.doctype.pf_coupon_book.pf_coupon_book_filter.list_filter",
    "PF Coupon Issue": "prasadam_flow.pf_manage.doctype.pf_coupon_issue.pf_coupon_issue_filter.list_filter",
}
#
has_permission = {
    "PF Coupon Transfer": "prasadam_flow.pf_manage.doctype.pf_coupon_transfer.pf_coupon_transfer_filter.single",
    "PF Coupon Book": "prasadam_flow.pf_manage.doctype.pf_coupon_book.pf_coupon_book_filter.single",
    "PF Coupon Issue": "prasadam_flow.pf_manage.doctype.pf_coupon_issue.pf_coupon_issue_filter.single",
}

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {"User": {"on_update": "prasadam_flow.controllers.user.on_update"}}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"prasadam_flow.tasks.all"
# 	],
# 	"daily": [
# 		"prasadam_flow.tasks.daily"
# 	],
# 	"hourly": [
# 		"prasadam_flow.tasks.hourly"
# 	],
# 	"weekly": [
# 		"prasadam_flow.tasks.weekly"
# 	],
# 	"monthly": [
# 		"prasadam_flow.tasks.monthly"
# 	],
# }
scheduler_events = {
    "cron": {
        "15 7 * * *": ["prasadam_flow.controllers.schedule_book.execute"],
    }
}

# Testing
# -------

# before_tests = "prasadam_flow.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "prasadam_flow.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "prasadam_flow.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["prasadam_flow.utils.before_request"]
# after_request = ["prasadam_flow.utils.after_request"]

# Job Events
# ----------
# before_job = ["prasadam_flow.utils.before_job"]
# after_job = ["prasadam_flow.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"prasadam_flow.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

website_route_rules = [{'from_route': '/prasadam_spw/<path:app_path>', 'to_route': 'prasadam_spw'},]