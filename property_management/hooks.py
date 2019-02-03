# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "property_management"
app_title = "Property Management"
app_publisher = "shakeel vaim"
app_description = "Property Management Application"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "shakeel.viam@rediumsys.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/property_management/css/property_management.css"
# app_include_js = "/assets/property_management/js/property_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/property_management/css/property_management.css"
# web_include_js = "/assets/property_management/js/property_management.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "property_management.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

calendars = ["Hall Contract"]

fixtures = ["Custom Field","Property Setter"]

# Installation
# ------------

# before_install = "property_management.install.before_install"
# after_install = "property_management.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "property_management.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"property_management.tasks.all"
	# ],
	"daily": [
		"property_management.property_management.doctype.rent_contract.rent_contract.update_status",
		"erpnext.hr.doctype.employee.employee.send_civil_id_expiry_notification",
		"erpnext.hr.doctype.employee.employee.send_passport_expiry_notification"
	]
	# ,
	# "hourly": [
	# 	"property_management.tasks.hourly"
	# ],
	# "weekly": [
	# 	"property_management.tasks.weekly"
	# ]
	# "monthly": [
	# 	"property_management.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "property_management.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "property_management.event.get_events"
# }

