frappe.email_alert = {
	setup_fieldname_select: function(frm) {
		// get the doctype to update fields
		if(!frm.doc.document_type) {
			return;
		}

		frappe.model.with_doctype(frm.doc.document_type, function() {

			var fields = frappe.get_doc("DocType", frm.doc.document_type).fields;

			var options = $.map(fields,
				function(d) { return in_list(frappe.model.no_value_type, d.fieldtype) ?
					null : d.fieldname; });

			options = options.join("\n");

			// set value changed options
			frm.set_df_property("value_changed", "options", "\n" + options);

			// set date changed options
			frm.set_df_property("date_changed", "options", $.map(fields,
				function(d) { return (d.fieldtype=="Date" || d.fieldtype=="Datetime") ?
					d.fieldname : null; }));

			// set email recipient options
			frappe.meta.get_docfield("Email Alert Recipient", "email_by_document_field",
				frm.doc.name).options = "\nowner\n" + options;

		});
	}
}

frappe.ui.form.on("Email Alert", "refresh", function(frm) {
	frappe.email_alert.setup_fieldname_select(frm);
});

frappe.ui.form.on("Email Alert", "document_type", function(frm) {
	frappe.email_alert.setup_fieldname_select(frm);
});
