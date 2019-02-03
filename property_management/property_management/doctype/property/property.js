// Copyright (c) 2016, shakeel vaim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Property', {
	refresh: function(frm) {
		cur_frm.toggle_enable(['building', 'property_type', 'block_number','street_name_number','area'], frm.doc.__islocal);
		if(!frm.doc.__islocal && frm.doc.rent) {
			frm.add_custom_button(__('Make Contract'),cur_frm.cscript.create_contract, __("Make"));
			frm.page.set_inner_btn_group_as_primary(__("Make"));
		}
	}
});

cur_frm.cscript.create_contract= function(frm) {
		frappe.model.open_mapped_doc({
			method: "property_management.property_management.doctype.property.property.create_contract",
			frm: cur_frm
		})
}