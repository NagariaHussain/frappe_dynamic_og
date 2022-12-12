# Copyright (c) 2022, Hussain Nagaria and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe_dynamic_og.core.generate_image import ImageGenerator


class EnabledTemplateAlreadyExistsException(Exception):
	"""An enabled OG Image Template Already exists"""

	pass


class OGImageTemplate(Document):
	def before_save(self):
		if self.has_value_changed("is_enabled"):
			self.validate_if_enabled_already_exists()

	def validate_if_enabled_already_exists(self):
		if self.is_enabled:
			enabled_exists = frappe.db.exists(
				"OG Image Template",
				{
					"for_doctype": self.for_doctype,
					"is_enabled": True,
					"name": ("!=", self.name),
				},
			)

			if enabled_exists:
				frappe.throw(
					"A template is already enabled for this doctype",
					EnabledTemplateAlreadyExistsException,
				)

	@frappe.whitelist()
	def generate_preview_image(self):
		image_generator = ImageGenerator(self, is_preview=True)
		file_doc = image_generator.generate()
		self.set("preview_image_file", file_doc.file_url)
		self.save()
