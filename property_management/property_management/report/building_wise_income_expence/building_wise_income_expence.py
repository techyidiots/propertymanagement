# Copyright (c) 2013, shakeel vaim and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns(filters)

	buildings=frappe.db.sql("select name from tabBuilding")

	data = []
	for building in buildings:
		row=[]
		row.append(building[0])
		income=frappe.db.sql("select sum(paid_amount) from `tabRent Receipt` where building='%s' and docstatus=1 "%(building[0]) ) [0][0] or 0.0
		row.append(income)
		expences=frappe.db.sql("select ifnull(sum(ecd.sanctioned_amount),0.0) from `tabExpense Claim` ec, `tabExpense Claim Detail` ecd where ec.name=ecd.parent and ec.approval_status='Approved' and ec.docstatus=1 and ec.building='%s' and ecd.expense_date between '%s' and '%s'"%(building[0],filters.get("from_date"),filters.get("to_date"))) [0][0] or 0.0
		row.append(expences)
		data.append(row)

	return columns, data

def get_columns(filters):
	"""return columns based on filters"""

	columns = [_("Building") + "::100"] + [_("Total Income") + ":Currency:150"] + [_("Total Expences") + ":Currency:150"]
	return columns
