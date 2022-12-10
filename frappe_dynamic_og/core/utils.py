import frappe

def generate_and_attach_og_image(doc, method=None):
    # TODO: DB call can be (and should be) prevented by caching
    # the list of docs for which the template is enabled
    # But for now, eh.

    # If there is a template and is enabled, only then proceed
    if not frappe.db.exists("OG Image Template", {"for_doctype": doc.doctype, "is_enabled": 1}):
        return
    
    frappe.errprint("There is a template and it is enabled.")