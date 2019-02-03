// Copyright (c) 2016, shakeel vaim and contributors
// For license information, please see license.txt

frappe.ui.form.on('Collect Rent', {
	onload: function(frm) {
		frm.doc.building = '';
		frm.doc.property = '';
		frm.doc.account = '';
		frm.set_query("property", function() {
				return {
					"filters": {
						"building": frm.doc.building
					}
				};
		});
		frm.set_query("account", function() {
				return {
					"filters": {
						"is_group": 0,
						"root_type":"Asset",
						"report_type":"Balance Sheet",
						"freeze_account":"No",
						"account_type":"Bank"
					}
				};
		});
	},

	refresh: function(frm) {
		frm.disable_save();
	}
});

//Create salary slip
//-----------------------
cur_frm.cscript.get_rent_receipts = function(doc, cdt, cdn) {
	frappe.call({
				method: "property_management.property_management.doctype.collect_rent.collect_rent.get_receipts",
				args: {
					building:cur_frm.doc.building,
					property_id:cur_frm.doc.property
				},
				callback: function(r, rt) {
					if(r.message) {
						employee_toolbar
						var employee_toolbar = $('<div class="col-sm-12 top-toolbar">\
							<button class="btn btn-default btn-add btn-xs"></button>\
							<button class="btn btn-xs btn-default btn-remove"></button>\
							<button class="btn btn-primary btn-mark-present btn-xs"></button>\
							</div>').appendTo(cur_frm.fields_dict.activity_log.wrapper);

						employee_toolbar.find(".btn-add")
							.html(__('Check all'))
							.on("click", function() {
								$(cur_frm.fields_dict.activity_log.wrapper).find('input[type="checkbox"]').each(function(i, check) {
									if(!$(check).is(":checked")) {
										check.checked = true;
									}
								});
							});

						employee_toolbar.find(".btn-remove")
							.html(__('Uncheck all'))
							.on("click", function() {
								$(cur_frm.fields_dict.activity_log.wrapper).find('input[type="checkbox"]').each(function(i, check) {
									if($(check).is(":checked")) {
										check.checked = false;
									}
								});
						});

						employee_toolbar.find(".btn-mark-present")
							.html(__('Collect Payment'))
							.on("click", function() {
								var employee_present = [];
								$(cur_frm.fields_dict.activity_log.wrapper).find('input[type="checkbox"]').each(function(i, check) {
									if($(check).is(":checked")) {
										employee_present.push(r.message[i]);
									}
								});
								frappe.call({
									method: "property_management.property_management.doctype.collect_rent.collect_rent.submit_rent_receipt",
									args:{
										"employee_list":employee_present,
										"account":cur_frm.doc.account
									},

									callback: function(r) {
										frappe.msgprint("Rent Collected Successfully...!")
										location.reload();
									}
								});
						});

						var row;
						$.each(r.message, function(i, m) {
							if (i===0 || (i % 2) === 0) {
								row = $('<div class="row"></div>').appendTo(cur_frm.fields_dict.activity_log.wrapper);
							}
							$(repl('<div class="col-sm-6 unmarked-employee-checkbox">\
								<div class="checkbox">\
								<label><input type="checkbox" class="employee-check" employee="%(employee)s"/>\
								ID:- %(employee)s &nbsp;&nbsp;&nbsp;Rent:- %(rent)s &nbsp;&nbsp;&nbsp;Tenant:- %(tenant)s</label>\
								</div></div>', {employee: r.message[i]['name'],rent:r.message[i]['final_rent_amount'],tenant:r.message[i]['customer']})).appendTo(row);
							});

					}
					else{
						frappe.msgprint("Rent Receipt Not Found or Rent Collected Already for Selected Criteria...!")
					}
			}
	})
}