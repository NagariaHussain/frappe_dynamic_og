import frappe

from subprocess import PIPE, Popen
from os.path import join as joinpath
from frappe.utils.caching import site_cache


class EnabledTemplateDoesNotExistException(Exception):
    """An enabled OG Image Template does not exist for a given doctype"""

    pass


class ImageGenerator:
    def __init__(self, doc, is_preview=False, is_debug_mode_on=False):
        self.doc = doc
        self.is_preview = is_preview
        self.is_debug_mode_on = is_debug_mode_on
        self.set_image_template()
        self.set_frappe_og_settings()

    def generate(self):
        """Generate OG image using the OG template for the doc and returns the file doc"""
        file_name = self.get_file_name()
        content = self.get_processed_html_content()
        stdout, stderr = generate_and_get_image_from_node_process(
            content, self.is_debug_mode_on
        )
        file_doc = None

        if not stderr:
            file_doc = self.create_image_file_doc(file_name, stdout)
        else:
            self.handle_node_process_error(stderr)

        if file_doc:
            self.delete_old_images_if_applicable(file_doc.name)

        return file_doc

    def set_image_template(self):
        if self.is_preview:
            # doc is itself the OG Template
            self.image_template = frappe._dict(
                {
                    "template_html": self.doc.template_html,
                    "attach_to_image_field": True,
                    "image_field": "preview_image_file",
                    "default_template_html": self.doc.default_template_html,
                    "use_default_template": self.doc.use_default_template,
                }
            )
            return

        self.image_template = frappe.db.get_value(
            "OG Image Template",
            {"for_doctype": self.doc.doctype, "is_enabled": 1},
            [
                "template_html",
                "attach_to_image_field",
                "image_field",
                "default_template_html",
                "use_default_template",
            ],
            as_dict=True,
        )

        if not self.image_template:
            frappe.throw(
                f"Enabled OG Image Template for doctype {self.doc.doctype} does not exist",
                EnabledTemplateDoesNotExistException,
            )

    def set_frappe_og_settings(self):
        if self.is_preview:
            self.frappe_og_settings = frappe._dict(
                {"automatically_delete_old_images": True, "optimise_images": False}
            )
            return

        self.frappe_og_settings = get_frappe_og_settings()

    def get_file_name(self):
        suffix = frappe.generate_hash(length=8)
        doc_info = frappe.scrub(f"{self.doc.doctype}_{self.doc.name}")
        return f"og_image_{doc_info}_{suffix}.png"

    def get_processed_html_content(self):
        html_template = self.get_html_template_from_image_template()
        if self.is_preview:
            # don't render jinja template if preview
            return html_template

        # render the jinja template using the doc
        content = frappe.render_template(html_template, {"doc": self.doc})
        return content.replace("\n", "")

    def get_html_template_from_image_template(self):
        if self.image_template.use_default_template:
            return self.image_template.default_template_html
        return self.image_template.template_html

    def create_image_file_doc(self, name, content):
        file_doc = frappe.new_doc("File")
        file_doc.file_name = name
        file_doc.content = content
        file_doc.attached_to_doctype = self.doc.doctype
        file_doc.attached_to_name = self.doc.name
        file_doc.attached_to_field = self.image_template.image_field

        if self.is_preview:
            file_doc.is_private = True

        file_doc.save()

        if self.image_template.attach_to_image_field:
            # set in database as well
            frappe.db.set_value(
                self.doc.doctype,
                self.doc.name,
                self.image_template.image_field,
                file_doc.file_url,
            )
            self.doc.set(self.image_template.image_field, file_doc.file_url)

        return file_doc

    def delete_old_images_if_applicable(self, new_file_doc_name):
        try:
            to_delete = self.frappe_og_settings.automatically_delete_old_images
            if to_delete:
                doc_info = frappe.scrub(f"{self.doc.doctype}_{self.doc.name}")
                old_image_files = frappe.db.get_all(
                    "File",
                    {"file_name": ("like", f"og_image_{doc_info}%")},
                    pluck="name",
                )
                for name in old_image_files:
                    if name == new_file_doc_name:
                        # this is the newly created file!
                        continue
                    frappe.delete_doc("File", name)
        except Exception:
            self.doc.log_error(
                "Error Deleting Old OG Images",
                "There was an error while deleting old OG images",
            )

    def handle_node_process_error(self, stderr):
        stderr = frappe.safe_decode(stderr)
        stderr = stderr.replace("\n", "<br>")
        error_message = f'<span>OG Image Generation Failed. </span><br><div style="font-family: monospace;">{stderr}</div>'
        self.doc.add_comment(text=error_message)
        self.doc.log_error("Error Generating OG Image", stderr)


def generate_and_attach_og_image(doc, method=None):
    # TODO: DB call can be (and should be) prevented by caching
    # the list of docs for which the template is enabled
    # But for now, eh.

    # If there is a template and is enabled, only then proceed
    if not frappe.db.exists(
        "OG Image Template", {"for_doctype": doc.doctype, "is_enabled": 1}
    ):
        return

    image_generator = ImageGenerator(doc)
    image_generator.generate()

    # for desk stuff!
    doc.reload()


def generate_and_get_image_from_node_process(html_content, is_debug_mode_on=False):
    command = ["node", "play.js", html_content]

    if is_debug_mode_on:
        command.append("--debug")

    process = Popen(
        command,
        cwd=frappe.get_app_path("frappe_dynamic_og", joinpath("..", "playground")),
        stdout=PIPE,
        stderr=PIPE,
    )

    return process.communicate()


@site_cache()
def get_frappe_og_settings():
    return frappe.db.get_singles_dict("Frappe Dynamic OG Settings", cast=True)
