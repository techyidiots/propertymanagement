# -*- coding: utf-8 -*-
# Copyright (c) 2015, shakeel vaim and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, formatdate, today, date_diff, nowdate
from frappe import _, msgprint
from frappe.model.naming import make_autoname
import erpnext

class RentContract(Document):

	def autoname(self):
		self.name = make_autoname(self.property + '-RC.###')
	
	def validate(self):
		if date_diff(self.contract_end_date, self.contract_start_date) < 0:
			frappe.throw(_("Rent Start Date cannot be before Rent End Date"))

		exist=frappe.db.sql("""select name,contract_start_date,contract_end_date from `tabRent Contract` where name<>'%s' and docstatus<> 2 and property='%s' and \
				(( contract_start_date<='%s' and contract_end_date>='%s') or ( contract_start_date>='%s' and contract_start_date<='%s') or 
				( contract_end_date>='%s' and contract_end_date<='%s'))
				"""%(self.name,self.property,self.contract_start_date,self.contract_end_date,self.contract_start_date,self.contract_end_date,self.contract_start_date,self.contract_end_date))
		if exist:
				frappe.throw(_("Rent Contract '{0}' with Contract Start Date '{1}' Contract End Date '{2}' Overlap with this contract for property '{3}'".format(exist[0][0],formatdate(exist[0][1]),formatdate(exist[0][2]),self.property)))


	def on_submit(self):
		if getdate(self.contract_start_date)<=getdate(today()) and getdate(self.contract_end_date)>=getdate(today()):
			frappe.db.set_value('Property',self.property,'status','Rented')

def update_status():
	rented=frappe.db.sql("select rc.property as property from `tabRent Contract` rc, tabProperty p where rc.property=p.name and p.status<>'Rented' and rc.contract_start_date=CURDATE()",as_dict=True)
	for record in rented:
		frappe.db.set_value('Property',record.get('property'),'status','Rented')

	available=frappe.db.sql("select rc.property as property from `tabRent Contract` rc, tabProperty p where rc.property=p.name and p.status='Rented' and rc.contract_end_date=date_add(CURDATE(),interval -1 day)",as_dict=True)
	for record in rented:
		frappe.db.set_value('Property',record.get('property'),'status','Available')


@frappe.whitelist()
def cancel_contract(rent_contract):
	frappe.db.set_value('Rent Contract',rent_contract,'contract_end_date',nowdate())
	return "Rent Contract '{0}' have Cancled Today. Contract End Date is '{1}'".format(rent_contract,formatdate(nowdate()))
