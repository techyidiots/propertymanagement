# -*- coding: utf-8 -*-
# Copyright (c) 2015, shakeel vaim and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import cint, cstr, nowdate
from erpnext.accounts.utils import get_fiscal_year
import calendar
import erpnext

class CollectRent(Document):
	pass

@frappe.whitelist()	
def get_receipts(building=None,property_id=None,tenant=None):
	condition=[]
	if building:
		condition.append(" building= '%s'"%(building))
	if property_id:
		condition.append(" property= '%s'"%(property_id))
	return frappe.db.sql("""select name,customer,final_rent_amount from `tabRent Receipt` where docstatus=0 and \
		 %s """%(" and ".join(r for r in condition)),as_dict=True)


@frappe.whitelist()	
def submit_rent_receipt(employee_list,account):
	records=eval(employee_list)
	from frappe.utils import money_in_words
	company=erpnext.get_default_company()
	currency=frappe.db.get_value('Company', company, 'default_currency')
	from erpnext.accounts.party import get_party_account
	for record in records:
		rr=frappe.get_doc("Rent Receipt",record['name'])
		rr.paid_amount=record['final_rent_amount']
		rr.paid_date=nowdate()
		je = frappe.new_doc("Journal Entry")
		je.voucher_type = "Journal Entry"
		je.posting_date = nowdate()
		je.company = company
		je.remark = "Entry against {0} worth {1}".format(record['name'], record['final_rent_amount'])

		je.append("accounts", {
			"account": get_party_account("Customer", record['customer'], company),
			"credit_in_account_currency": record['final_rent_amount'],
			"reference_type": "Rent Receipt",
			"reference_name": record['name'],
			"party":record["customer"],
			"party_type":"Customer"
		})

		je.append("accounts", {
			"account": account,
			"debit_in_account_currency": record['final_rent_amount'],
			"reference_type": "Rent Receipt",
			"reference_name": record['name'],
			"cost_center": frappe.db.get_value('Company', company, 'cost_center')

		})

		je.flags.ignore_permissions = True
		je.submit()
		rr.rent_received_against=je.name
		rr.submit()

