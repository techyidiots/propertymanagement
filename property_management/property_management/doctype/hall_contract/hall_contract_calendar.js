frappe.views.calendar["Hall Contract"] = {
	field_map: {
		"start": "starts_on",
		"end": "ends_on",
		"id": "name",
		"title": "name",
		"allDay": "allDay",
		"status":"docstatus"
	},
	style_map: {
		"0": "info", 
		"1": "success", 
		"2": "danger"
	},
	get_events_method: "property_management.property_management.doctype.hall_contract.hall_contract.get_events"
}