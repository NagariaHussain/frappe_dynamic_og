import frappe

from os.path import abspath
from subprocess import PIPE, Popen
from os.path import join as join_path

# will be the doc
self = frappe._dict({
    "title": "WhatsApp Integration",
    "name": "whatsapp_integration"
})

# will come from the og image template
doctype_name = "Marketplace App"

template_html = """
<div style="color: white; height: 100vh; width: 100%; display: flex; align-items: center; justify-content: center; flex-direction: column">    
    <h1 style="font-size: 40px">{{doc.title}}</h1>
    <h2 style="font-size: 20px">{{doc.name}}</h2>
</div>
"""

suffix = frappe.generate_hash(length=8)

# Maybe add document name too?
file_name = f"og_image_{frappe.scrub(doctype_name)}_{suffix}.png"

content = frappe.render_template(template_html, {"doc": self})
content = content.replace("\n", "")

command = ["node", "play.js", content]

process = Popen(command, cwd=frappe.get_app_path("frappe_dynamic_og", "../playground"), stdout=PIPE, stderr=PIPE)

stdout = process.communicate()[0]
stderr = process.communicate()[1]

if not stderr:
    file_doc = frappe.new_doc("File")
    file_doc.file_name = file_name
    file_doc.content = stdout
    # TODO: Replace with Actual Values from self
    file_doc.attached_to_doctype = "ToDo"
    file_doc.attached_to_name = "f03a0fdbf8"
    file_doc.save()