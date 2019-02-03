# -*- coding: utf-8 -*-
# Copyright (c) 2015, shakeel vaim and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import erpnext
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import formatdate, date_diff, nowdate
from frappe import _, msgprint
from erpnext.accounts.utils import get_fiscal_year

class HallContract(Document):
	def autoname(self):
		self.name = make_autoname(self.customer+ "/" + formatdate(self.starts_on) + "/.##")

	def validate(self):
		if date_diff(self.ends_on, self.starts_on) < 0:
			frappe.throw(_("Hall Contrat Start DateTime cannot be before Hall Contract End DateTime..!"))

		exist=frappe.db.sql("""select name,starts_on,ends_on from `tabHall Contract` where name<>'%s' and docstatus<> 2 and \
				(( starts_on<='%s' and ends_on>='%s') or ( starts_on>='%s' and starts_on<='%s') or 
				( ends_on>='%s' and ends_on<='%s'))
				"""%(self.name,self.starts_on,self.ends_on,self.starts_on,self.ends_on,self.starts_on,self.ends_on))
		if exist:
				frappe.throw(_("Hall Contract '{0}' with Contract Start DateTime '{1}' Contract End DateTime '{2}' Overlap with this contract..!".format(exist[0][0],formatdate(exist[0][1]),formatdate(exist[0][2]))))

	def before_cancel(self):
		frappe.db.sql("delete from `tabGL Entry` where voucher_type='Hall Contract' and voucher_no='%s'"%(self.name))

	def on_trash(self):
		frappe.db.sql("delete from `tabGL Entry` where voucher_type='Hall Contract' and voucher_no='%s'"%(self.name))

	def on_submit(self):
			company=erpnext.get_default_company()
			currency=frappe.db.get_value('Company', company, 'default_currency')
			from erpnext.accounts.party import get_party_account
			account=frappe.db.sql("select default_account from `tabMode of Payment Account`  where parent='%s' and company='%s'"%(self.mode_of_payment,company))
			if not account:
				frappe.throw(_("Please Select default account in mode of payment for {0}".format(self.mode_of_payment)))

			if account:
				je = frappe.new_doc("Journal Entry")
				je.voucher_type = "Journal Entry"
				je.posting_date = nowdate()
				je.company = company
				je.remark = "Entry against {0} worth {1}".format(self.name, self.rent)

				je.append("accounts", {
					"account": get_party_account("Customer", self.customer, company),
					"credit_in_account_currency": self.rent,
					"reference_type": "Hall Contract",
					"reference_name": self.name,
					"party":self.customer,
					"party_type":"Customer"
				})

				je.append("accounts", {
					"account": account[0][0],
					"debit_in_account_currency": self.rent,
					"reference_type": "Hall Contract",
					"reference_name": self.name,
					"cost_center": frappe.db.get_value('Company', company, 'cost_center')

				})
				je.flags.ignore_permissions = True
				je.submit()
				frappe.db.set_value("Hall Contract",self.name,'payment_received_against',je.name)


	def on_update(self):
		already_created=frappe.db.sql("select name from `tabGL Entry` where voucher_type='Hall Contract' and voucher_no='%s' "%(self.name))
		if not already_created and self.docstatus==0:
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
					'voucher_type': "Hall Contract",
					'voucher_no': self.name,
					'remarks': "Hall Rent",
					'debit': self.rent,
					'credit': 0,
					'debit_in_account_currency': self.rent,
					'credit_in_account_currency': 0,
					'is_opening': "No",
					'party_type': "Customer",
					'party': self.customer,
					'project': None
			})
			gldict_debit.insert()
			gldict_credit = frappe.get_doc({
				    'doctype': 'GL Entry',
					'company': default_company,
					'posting_date': nowdate(),
					'account': default_income_account,
					'fiscal_year': get_fiscal_year(nowdate(), company=default_company)[0],
					'voucher_type': "Hall Contract",
					'voucher_no': self.name,
					'remarks': "Hall Rent",
					'cost_center':default_cost_center,
					'debit': 0,
					'credit': self.rent,
					'debit_in_account_currency': 0,
					'credit_in_account_currency': self.rent,
					'is_opening': "No",
					'against':self.customer,
					'party_type': None,
					'party': None,
					'project': None
			})
			gldict_credit.insert()

@frappe.whitelist()
def get_events(start, end, user=None):
	if not user:
		user = frappe.session.user
	return  frappe.db.sql("""select name,
		starts_on, ends_on, all_day, docstatus
		from `tabHall Contract`
 where ((
			(date(starts_on) between date(%(start)s) and date(%(end)s))
			or (date(ends_on) between date(%(start)s) and date(%(end)s))
			or (date(starts_on) <= date(%(start)s) and date(ends_on) >= date(%(end)s))
		) or (
			date(starts_on) <= date(%(start)s) 
		))
		order by starts_on""", {
			"start": start,
			"end": end,
			"user": user,
		}, as_dict=1)