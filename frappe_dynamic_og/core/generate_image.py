import frappe

from subprocess import PIPE, Popen


def generate_and_attach_og_image(doc, method=None):
    # TODO: DB call can be (and should be) prevented by caching
    # the list of docs for which the template is enabled
    # But for now, eh.

    # If there is a template and is enabled, only then proceed
    if not frappe.db.exists(
        "OG Image Template", {"for_doctype": doc.doctype, "is_enabled": 1}
    ):
        return

    content = get_processed_html_content(doc)
    stdout, stderr = generate_and_get_image_from_node_process(content)

    if not stderr:
        create_file_doc(get_file_name(doc), stdout, doc.doctype, doc.name)


def create_file_doc(name, content, attached_to_doctype, attached_to_name):
    file_doc = frappe.new_doc("File")
    file_doc.file_name = name
    file_doc.content = content
    file_doc.attached_to_doctype = attached_to_doctype
    file_doc.attached_to_name = attached_to_name
    file_doc.save()


def get_file_name(doc):
    suffix = frappe.generate_hash(length=8)
    doc_info = frappe.scrub(f"{doc.doctype}_{doc.name}")
    return f"og_image_{doc_info}_{suffix}.png"


def get_processed_html_content(doc):
    template_html = frappe.db.get_value(
        "OG Image Template",
        {"for_doctype": doc.doctype, "is_enabled": 1},
        "template_html",
    )
    content = frappe.render_template(template_html, {"doc": doc})
    return content.replace("\n", "")


def generate_and_get_image_from_node_process(html_content):
    command = ["node", "play.js", html_content]

    process = Popen(
        command,
        cwd=frappe.get_app_path("frappe_dynamic_og", "../playground"),
        stdout=PIPE,
        stderr=PIPE,
    )

    return process.communicate()
