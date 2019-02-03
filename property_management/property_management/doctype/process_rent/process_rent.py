# -*- coding: utf-8 -*-
# Copyright (c) 2015, shakeel vaim and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import cint, cstr, nowdate, money_in_words, date_diff, add_months, getdate
from erpnext.accounts.utils import get_fiscal_year
import calendar
import erpnext

class ProcessRent(Document):
	pass

@frappe.whitelist()	
def set_dates():
		import datetime
 		today = datetime.date.today()
 		last = today.replace(day=1) - datetime.timedelta(days=1)
 		first=last.replace(day=1)
 		return first,last

@frappe.whitelist()	
def create_rent_receipts(from_period,to_period,building=None,property_id=None,tenant=None):
	"""
		Creates salary slip for selected employees if already not created
	"""
	ss_list=[]
	company=erpnext.get_default_company()
	currency=frappe.db.get_value('Company', company, 'default_currency')
	contract_list=get_receipts(from_period,to_period,building,property_id,tenant)
	for record in contract_list:
		exist=frappe.db.sql("select name from `tabRent Receipt` where rent_contract_id='%s' and from_period='%s' and to_period='%s' "%(record.get('name'),from_period,to_period))
		if not exist:
			ss = frappe.get_doc({
							"doctype": "Rent Receipt",
							"rent_contract_id": record.get('name'),
							"property":record.get('property'),
							"property_type":record.get('property_type'),
							"building":record.get('building'),
							"block_number":record.get("block_number"),
							"street_name_number":record.get("street_name_number"),
							"area":record.get('area'),
							"customer":record.get('tenant'),
							"tenant_name":record.get("tenant_name"),
							"agreement_start_date":record.get('contract_start_date'),
							"agreement_end_date":record.get('contract_end_date'),
							"rent_amount":record.get('rent'),
							"rent_amount_in_words":record.get('rent_amount_in_words'),
							"final_rent_amount":record.get('final_rent_amount'),
							"from_period": from_period,
							"to_period": to_period
			})
			ss.insert()
			make_gl_entry(ss.customer,ss.final_rent_amount,ss.name)
			ss_list.append(ss.name)
	return create_log(ss_list)

def make_gl_entry(tenant,final_rent_amount,name):
	from erpnext.accounts.general_ledger import make_gl_entries
	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	default_receivable_account=frappe.db.get_value("Company",default_company,"default_receivable_account")
	default_income_account=frappe.db.get_value("Company",default_company,"default_income_account")
	default_cost_center=frappe.db.get_value("Company",default_company,"cost_center")
	gldict_debit =frappe.get_doc( {
		    'doctype': 'GL Entry',
			'company': default_company,
			'account': default_receivable_account,
			'against': default_income_account,
			'posting_date': nowdate(),
			'fiscal_year': get_fiscal_year(nowdate(), company=default_company)[0],
			'voucher_type': "Rent Receipt",
			'voucher_no': name,
			'remarks': "Monthly Rent",
			'debit': final_rent_amount,
			'credit': 0,
			'debit_in_account_currency': final_rent_amount,
			'credit_in_account_currency': 0,
			'is_opening': "No",
			'party_type': "Customer",
			'party': tenant,
			'project': None
	})
	gldict_debit.insert()
	gldict_credit = frappe.get_doc({
		    'doctype': 'GL Entry',
			'company': default_company,
			'posting_date': nowdate(),
			'account': default_income_account,
			'fiscal_year': get_fiscal_year(nowdate(), company=default_company)[0],
			'voucher_type': "Rent Receipt",
			'voucher_no': name,
			'remarks': "Monthly Rent",
			'cost_center':default_cost_center,
			'debit': 0,
			'credit': final_rent_amount,
			'debit_in_account_currency': 0,
			'credit_in_account_currency': final_rent_amount,
			'is_opening': "No",
			'against':tenant,
			'party_type': None,
			'party': None,
			'project': None
	})
	gldict_credit.insert()

	return ""
@frappe.whitelist()	
def get_receipts(from_period,to_period,building=None,property_id=None,tenant=None):
	condition=[]
	if building:
		condition.append(" building= '%s'"%(building))
	if property_id:
		condition.append(" property= '%s'"%(property_id))
	if tenant:
		condition.append(" tenant= '%s'"%(tenant))
	condition.append(" contract_start_date<= '%s'"%(from_period))
	condition.append(" contract_end_date>= '%s'"%(to_period))
	return frappe.db.sql("""select name,property,property_type,building,block_number,street_name_number,area,tenant,\
		tenant_name,contract_start_date,contract_end_date,rent,final_rent_amount,rent_amount_in_words from `tabRent Contract` where docstatus=1 and \
		 %s """%(" and ".join(r for r in condition)),as_dict=True)

def create_log(ss_list):
	log = "<p>" + _("No Rent Contract Found for the above selected criteria OR Rent Receipt already created") + "</p>"
	if ss_list:
		log = "<b>" + _("Rent Receipts Created") + "</b>\
		<br><br>%s" % '<br>'.join(format_as_links(ss_list))
	return log


def format_as_links(ss_list):
		return ['<a href="#Form/Rent Receipt/{0}">{0}</a>'.format(s) for s in ss_list]


@frappe.whitelist()	
def print_receipts(from_period,to_period,building=None,property_id=None,tenant=None):
	contract_dict=get_receipts(from_period,to_period,building,property_id,tenant)
	dictList=[]
	for r in contract_dict:
		dictList.append(r['name'])
	exist=frappe.db.sql("select name from `tabRent Receipt` where rent_contract_id in ('%s') and from_period='%s' and to_period='%s' "%("','".join([r for r in dictList]),from_period,to_period))
	return [r[0] for r in exist]


@frappe.whitelist()	
def get_customer_name(tenant):
	name=frappe.db.sql("select trim(concat(customer_name,' ',second_name,' ',third_name)) from tabCustomer where name='%s'"%(tenant))
	return name

def tenant_query(doctype, txt, searchfield, start, page_len, filters):
	condition=[]
	condition.append(" tenant LIKE '%s' " %("%%%s%%" % txt))
	if filters.get("building"):
		condition.append(" building = '%s'"%(filters.get("building")))
	if filters.get("property"):
		condition.append(" property = '%s'"%(filters.get("property")))
	tenant = frappe.db.sql("""select distinct tenant from `tabRent Contract`
		where %s"""%(" and ".join(cond for cond in condition)))
	return tenant
