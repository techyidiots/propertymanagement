# -*- coding: utf-8 -*-
# Copyright (c) 2015, shakeel vaim and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import throw, _

class Year(Document):
	
	def validate(self):
		import re
		if not re.match("^[0-9]{4}$", self.year):
			throw(_("Year '{0}' Must be four digits only. Please Verify..!").format(self.year))
		if self.year=='0000':
			throw(_("Invalid Year '{0}'. Please Verify..!").format(self.year))
