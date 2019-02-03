// Copyright (c) 2016, shakeel vaim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rent Contract', {
	refresh: function(frm) {
		frm.add_fetch('property','property_type','property_type');
		frm.add_fetch('property','building','building');
		frm.add_fetch('property','rent','rent');
		frm.add_fetch('property','block_number','block_number');
		frm.add_fetch('property','street_name_number','street_name_number');
		frm.add_fetch('property','area','area');
		frm.add_fetch('tenant','mobile_number','mobile_number');
		frm.add_fetch('tenant','civil_id','civil_id');
		frm.add_fetch('tenant','occupation','occupation');
		if (frm.doc.__islocal){
			frm.set_value("date",frappe.datetime.get_today());

		}
		if(frm.doc.docstatus==1 && frm.doc.contract_start_date <= frappe.datetime.get_today() && frm.doc.contract_end_date > frappe.datetime.get_today() ) {
			frm.add_custom_button(__('Cancel Contract'),cur_frm.cscript.cancel_contract, __("Make"));
			frm.page.set_inner_btn_group_as_primary(__("Make"));
		}

	},
	property: function(frm) {
		frm.set_value("final_rent_amount", parseFloat(frm.doc.rent)-parseFloat(frm.doc.discount));
	},
	discount: function(frm) {
		frm.set_value("final_rent_amount", parseFloat(frm.doc.rent)-parseFloat(frm.doc.discount));
	},
	final_rent_amount: function(frm) {
		frm.set_value("rent", parseFloat(frm.doc.final_rent_amount)-parseFloat(frm.doc.discount));
	},
	tenant: function(frm) {
		frappe.call({
				method: "property_management.property_management.doctype.process_rent.process_rent.get_customer_name",
				args: {
					tenant: cur_frm.doc.tenant,
				},
				callback: function(r, rt) {
					if(r.message) {
						frm.set_value("tenant_name",r.message[0][0]);
					}
				}
		})
	},
	contract_start_date: function(frm) {
		frm.set_value("contract_end_date", frappe.datetime.add_days(frappe.datetime.add_months(frm.doc.contract_start_date, 60), -1))
	}
});

cur_frm.cscript.cancel_contract= function(frm) {
		frappe.call({
				method: "property_management.property_management.doctype.rent_contract.rent_contract.cancel_contract",
				args: {
					rent_contract: cur_frm.doc.name,
				},
				callback: function(r, rt) {
					if(r.message) {
						frappe.msgprint(__(r.message));
						location.reload();
					}
				}
		})
}
