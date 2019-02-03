# -*- coding: utf-8 -*-
# Copyright (c) 2015, shakeel vaim and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cstr
from frappe.model.naming import make_autoname

class RentReceipt(Document):

	def autoname(self):
		self.name = make_autoname(self.rent_contract_id+ "/.###")

	def before_cancel(self):
		frappe.db.sql("delete from `tabGL Entry` where voucher_type='Rent Receipt' and voucher_no='%s'"%(self.name))

	def on_trash(self):
		frappe.db.sql("delete from `tabGL Entry` where voucher_type='Rent Receipt' and voucher_no='%s'"%(self.name))
	
