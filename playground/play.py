import scrub

from os.path import abspath
from subprocess import PIPE, Popen
from os.path import join as join_path

# will be the doc
self = None
doctype_name = "Marketplace App"

# will come from the og image template
template_html = ""

# Sample: '/Users/mdhussain/Frappe/bench-0/sites/abc.localhost/public/files/frappe_og_images'
folder_path = abspath(frappe.utils.get_files_path("frappe_og_images", is_private=False))

# Create folder path if not exists
frappe.create_folder(folder_path)

suffix = frappe.generate_hash(length=8)
file_name = f"og_image_{frappe.scrub(doctype_name)}_{suffix}.png"

output_path = join_path(folder_path, file_name)

content = frappe.render_template(template_html, {"doc": self})
content = content.replace("\n", "\\n")

command = ["node", "play.js", output_path, content]

process = Popen(command, cwd=frappe.get_app_path("frappe_dynamic_og", "playground"), stdout=PIPE, stderr=PIPE)

frappe.msgprint(_("Compiled Successfully"), alert=True)