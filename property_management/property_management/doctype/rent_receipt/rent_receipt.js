// Copyright (c) 2016, shakeel vaim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rent Receipt', {
	refresh: function(frm) {
		frm.add_fetch('rent_contract_id','property_type','property_type');
		frm.add_fetch('rent_contract_id','building','building');
		frm.add_fetch('rent_contract_id','final_rent_amount','final_rent_amount');
		frm.add_fetch('rent_contract_id','area','area');
		frm.add_fetch('rent_contract_id','area_unit','area_unit');
		frm.add_fetch('rent_contract_id','agreement_start_date','agreement_start_date');
		frm.add_fetch('rent_contract_id','tenant','customer');
		frm.add_fetch('rent_contract_id','agreement_end_date','agreement_end_date');
	}
});
