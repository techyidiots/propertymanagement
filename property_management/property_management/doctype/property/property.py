# -*- coding: utf-8 -*-
# Copyright (c) 2015, shakeel vaim and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.model.mapper import get_mapped_doc

class Property(Document):
		
	def autoname(self):
		self.name = make_autoname(self.building + '-P.###')




@frappe.whitelist()
def create_contract(source_name, target_doc=None):
	doclist = get_mapped_doc("Property", source_name,
		{"Property": {
			"doctype": "Rent Contract",
			"field_map": {
				"name": "property",
				"property_type": "property_type",
				"building":"building",
				"block_number": "block_number",
				"street_name_number": "street_name_number",
				"area": "area",
				"rent": "rent",
				"rent":"final_rent_amount"
			}
		}}, target_doc, ignore_permissions=True)

	return doclist