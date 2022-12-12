// Copyright (c) 2022, Hussain Nagaria and contributors
// For license information, please see license.txt

frappe.ui.form.on("OG Image Template", {
  refresh(frm) {},
  template_html(frm) {
    // runs on change
    // console.log("template_html changed.")
  },
  is_debug_mode_on(frm) {
    generate_preview_image(frm);
  },
  generate_preview_button(frm) {
    generate_preview_image(frm);
  },
});

function generate_preview_image(frm) {
  frm.call("generate_preview_image").then(() => {
    frappe.show_alert({
      message: "Preview Image Updated",
      indicator: "green",
    });
  });
}
