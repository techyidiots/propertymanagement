from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Property Masters"),
			"items": [
				{
					"type": "doctype",
					"name": "Year",
					"description": _("Year Master."),
				},
				{
					"type": "doctype",
					"name": "Property Type",
					"description": _("Property Type Master."),
				},
				{
					"type": "doctype",
					"name": "Building",
					"label": _("Building"),
					"description": _("Building Master."),
				},
				{
					"type": "doctype",
					"name": "Property",
					"description": _("Property Master."),
				},
				{
					"type": "doctype",
					"name": "Salutation",
					"description": _("Salutation Master."),
				},
				{
					"type": "doctype",
					"name": "Add New Properties",
					"description": _("Add New Properties."),
				},
				{
					"type": "doctype",
					"name": "Phone Book",
					"description": _("Add Phone Book."),
				},	
			]
		},
		{
			"label": _("Property Records"),
			"items": [
				{
					"type": "doctype",
					"name": "Rent Contract",
					"label": _("Rent Contract"),
					"description": _("Rent Contract Records."),
				},
				{
					"type": "doctype",
					"name": "Rent Receipt",
					"label": _("Rent Receipt"),
					"description": _("Rent Receipt Records."),
				},
				{
					"type": "doctype",
					"name": "Process Rent",
					"label": _("Process Rent"),
					"description": _("Process Rent (Generate Rent Receipts and Print)."),
				},
				{
					"type": "doctype",
					"name": "Process Rent for Commerital",
					"label": _("Process Rent for Commerital Properties"),
					"description": _("Process Rent for Commerital Properties (Generate Rent Receipts and Print)."),
				},
				{
					"type": "doctype",
					"name": "Collect Rent",
					"label": _("Collect Rent"),
					"description": _("Collect Rent."),
				},
				{
					"type": "doctype",
					"name": "Hall Contract",
					"label": _("Hall Contract"),
					"description": _("Hall Contract."),
				},
			]
		}
	]
