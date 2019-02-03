// Copyright (c) 2016, shakeel vaim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Year', {
	refresh: function(frm) {
		if(frm.doc.__islocal) {
		frm.set_value("year", moment(frappe.datetime.nowdate()).format("YYYY"));
		}
	}
});
