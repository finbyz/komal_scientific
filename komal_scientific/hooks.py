app_name = "komal_scientific"
app_title = "Komal Scientific"
app_publisher = "Mukesh"
app_description = "Komal Scientific"
app_email = "info@finbyz.tech"
app_license = "gpl-3.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "komal_scientific",
# 		"logo": "/assets/komal_scientific/logo.png",
# 		"title": "Komal Scientific",
# 		"route": "/komal_scientific",
# 		"has_permission": "komal_scientific.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/komal_scientific/css/komal_scientific.css"
# app_include_js = "/assets/komal_scientific/js/komal_scientific.js"

# include js, css files in header of web template
# web_include_css = "/assets/komal_scientific/css/komal_scientific.css"
# web_include_js = "/assets/komal_scientific/js/komal_scientific.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "komal_scientific/public/scss/website"

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
# app_include_icons = "komal_scientific/public/icons.svg"

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
# 	"methods": "komal_scientific.utils.jinja_methods",
# 	"filters": "komal_scientific.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "komal_scientific.install.before_install"
# after_install = "komal_scientific.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "komal_scientific.uninstall.before_uninstall"
# after_uninstall = "komal_scientific.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "komal_scientific.utils.before_app_install"
# after_app_install = "komal_scientific.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "komal_scientific.utils.before_app_uninstall"
# after_app_uninstall = "komal_scientific.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "komal_scientific.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"before_naming": "komal_scientific.komal_scientific.doc_events.sales_invoice.autoname",
		"autoname": "komal_scientific.komal_scientific.doc_events.sales_invoice.autoname",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"komal_scientific.tasks.all"
# 	],
# 	"daily": [
# 		"komal_scientific.tasks.daily"
# 	],
# 	"hourly": [
# 		"komal_scientific.tasks.hourly"
# 	],
# 	"weekly": [
# 		"komal_scientific.tasks.weekly"
# 	],
# 	"monthly": [
# 		"komal_scientific.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "komal_scientific.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "komal_scientific.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "komal_scientific.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["komal_scientific.utils.before_request"]
# after_request = ["komal_scientific.utils.after_request"]

# Job Events
# ----------
# before_job = ["komal_scientific.utils.before_job"]
# after_job = ["komal_scientific.utils.after_job"]

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
# 	"komal_scientific.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
fixtures = [
    {
        "dt": "Property Setter",
        "filters": {"name": ["in", ["Sales Invoice-main-naming_rule","Sales Invoice-naming_series-options"]]},
    }
]
# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

