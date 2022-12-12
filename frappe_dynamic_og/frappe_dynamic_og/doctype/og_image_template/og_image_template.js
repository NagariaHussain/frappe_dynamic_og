// Copyright (c) 2022, Hussain Nagaria and contributors
// For license information, please see license.txt

frappe.ui.form.on("OG Image Template", {
  refresh(frm) {},
  template_html(frm) {
    // runs on change
    // console.log("template_html changed.")
  },
  generate_preview_button(frm) {
    console.log("button clicked.");
  },
});
