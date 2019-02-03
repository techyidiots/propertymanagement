// Copyright (c) 2016, shakeel vaim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Process Rent for Commerital', {
	onload: function(frm) {  
		frm.doc.building = '';
		frm.doc.property = '';
		frm.doc.tenant = '';
		frm.set_query("property", function() {
				return {
					"filters": {
						"building": frm.doc.building
					}
				};
		});
		frm.set_query("tenant", function() {
				return {
					query: "property_management.property_management.doctype.process_rent_for_commerital.process_rent_for_commerital.tenant_query",
					filters: {
						"building": frm.doc.building,
						"property": frm.doc.property
					}
				}
		});
	},

	refresh: function(frm) {
		frm.disable_save();
	},
	from_period: function(frm) {
		if (cur_frm.doc.to_period){
			frm.trigger("to_period");
		}
	},
	to_period: function(frm) {
		if (cur_frm.doc.from_period && cur_frm.doc.to_period){
			frappe.call({
				method: "property_management.property_management.doctype.process_rent_for_commerital.process_rent_for_commerital.get_rent",
				args: {
					property_id:cur_frm.doc.property,
					from_period: cur_frm.doc.from_period,
					to_period:cur_frm.doc.to_period
				},
				callback: function(r, rt) {
					if(r.message) {
						cur_frm.set_value("rent_amount",r.message[0]);
						cur_frm.set_value("tenant",r.message[1][0][0]);
					}
				}
			})
		}
	}
});

cur_frm.cscript.display_activity_log = function(msg) {
	if(!cur_frm.ss_html)
		cur_frm.ss_html = $a(cur_frm.fields_dict['activity_log'].wrapper,'div');
	if(msg) {
		cur_frm.ss_html.innerHTML =
			'<div class="padding"><h4>'+__("Activity Log:")+'</h4>'+msg+'</div>';
	} else {
		cur_frm.ss_html.innerHTML = "";
	}
}


//Create salary slip
//-----------------------
cur_frm.cscript.create_rent_receipts = function(doc, cdt, cdn) {
	if (cur_frm.doc.rent_amount==undefined){
		frappe.msgprint(__("No Rent Contract Found for the above selected criteria OR Rent Receipt already created....!"))
		cur_frm.cscript.display_activity_log("");
	}
	else if (cur_frm.doc.property=='' || cur_frm.doc.from_period==undefined || cur_frm.doc.to_period==undefined || cur_frm.doc.rent_amount_in_words==undefined){
		frappe.msgprint(__("Property, From Period, To Period and Amount in Words in mandatory....!"))
		cur_frm.cscript.display_activity_log("");
	}
	else{
		cur_frm.cscript.display_activity_log("");
		frappe.call({
			method: "property_management.property_management.doctype.process_rent_for_commerital.process_rent_for_commerital.create_rent_receipts",
			args: {
				from_period: cur_frm.doc.from_period,
				to_period:cur_frm.doc.to_period,
				building:cur_frm.doc.building,
				property_id:cur_frm.doc.property,
				tenant:cur_frm.doc.tenant,
				rent:cur_frm.doc.rent_amount,
				rent_amount_in_words:cur_frm.doc.rent_amount_in_words
			},
			callback: function(r, rt) {
				if(r.message) {
					cur_frm.cscript.display_activity_log(r.message);
				}
			}
		})
	}
}

cur_frm.cscript.print_rent_receipts = function(doc, cdt, cdn) {
	frappe.call({
				method: "property_management.property_management.doctype.process_rent_for_commerital.process_rent_for_commerital.print_receipts",
				args: {
					building:cur_frm.doc.building,
					property_id:cur_frm.doc.property,
					tenant:cur_frm.doc.tenant,
					from_period: cur_frm.doc.from_period,
					to_period:cur_frm.doc.to_period
				},
				callback: function(r, rt) {
					if(r.message) {
						var json_string = JSON.stringify(r.message);
						var w = window.open("/api/method/frappe.utils.print_format.download_multi_pdf?"
							+"doctype="+encodeURIComponent('Rent Receipt')
							+"&name="+encodeURIComponent(json_string)
							+"&format="+encodeURIComponent('Rent Receipt')
							+"&no_letterhead=0");
						if(!w) {
							msgprint(__("Please enable pop-ups")); return;
						}
					}
				}
	})	
}