// Copyright (c) 2022, Hussain Nagaria and contributors
// For license information, please see license.txt

const DEFAULT_TEMPLATE = `<div style="display: flex; background-color: #fff; color: #313B44; height: 100vh; width: 100%; align-items: center; justify-content: center; flex-direction: column;"> 
  <span style="font-size: 60px; font-style: semibold; color: #74808B; text-transform: uppercase;">{{ doc.doctype }}</span>
  <h1 style="font-size: 120px; font-style: bold;">{{ doc.get_title() }}</h1>
  <img src="https://frappeframework.com/files/frappeframework-logo2a3e81.png" style="position: absolute; height: 40px; left: 40px; top: 40px;">
</div>`;

frappe.ui.form.on("OG Image Template", {
  refresh(frm) {
    const btn = frm.add_custom_button(
      "Generate Images For Existing Documents",
      () => {
        frm
          .call({
            doc: frm.doc,
            method: "generate_images_for_existing_documents",
            btn: btn,
          })
          .then(() => {
            frappe.show_alert({
              message: "Image Generation Complete!",
              indicator: "green",
            });
          });
      }
    );
  },
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
  use_default_template(frm) {
    if (frm.doc.use_default_template) {
      frm.set_value("template_html", DEFAULT_TEMPLATE);
    }
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
