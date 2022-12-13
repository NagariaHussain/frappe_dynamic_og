# Copyright (c) 2022, Hussain Nagaria and Contributors
# See license.txt

import frappe

from frappe.tests.utils import FrappeTestCase
from frappe.core.api.file import get_attached_images

from frappe_dynamic_og.frappe_dynamic_og.doctype.og_image_template.og_image_template import (
	EnabledTemplateAlreadyExistsException,
	OGImageTemplate,
)


class TestOGImageTemplate(FrappeTestCase):
	def setUp(self):
		# Disable any existing template
		frappe.db.set_value(
			"OG Image Template", {"is_enabled": True}, "is_enabled", False
		)

	def test_no_more_than_one_enabled_template_at_a_time(self):
		test_template_1 = frappe.get_doc(
			{
				"doctype": "OG Image Template",
				"for_doctype": "ToDo",
				"is_enabled": True,
				"template_html": "test",
			}
		).insert()

		test_template_2 = frappe.get_doc(
			{
				"doctype": "OG Image Template",
				"for_doctype": "ToDo",
				"is_enabled": True,
				"template_html": "test2",
			}
		)

		with self.assertRaises(EnabledTemplateAlreadyExistsException):
			test_template_2.insert()

		# Now, disabled the first one
		test_template_1.is_enabled = False
		test_template_1.save()

		# Second one should save successfully now
		test_template_2.insert()

	def test_preview_generation(self):
		test_template: OGImageTemplate = frappe.get_doc(
			{
				"doctype": "OG Image Template",
				"for_doctype": "ToDo",
				"is_enabled": True,
				"template_html": "test",
			}
		).insert()

		test_template.generate_preview_image()

		# preview image should be generated and attached
		preview_image_url = test_template.preview_image_file
		self.assertIsNotNone(preview_image_url)
		self.assertIsInstance(preview_image_url, str)

		# the image should be private
		file_is_private = frappe.db.get_value(
			"File",
			{"file_url": preview_image_url},
			"is_private",
		)
		self.assertTrue(file_is_private)

	def test_generate_images_for_existing_images_api(self):
		test_todo_doc = frappe.get_doc(
			{"doctype": "ToDo", "description": "test"}
		).insert()

		test_template: OGImageTemplate = frappe.get_doc(
			{
				"doctype": "OG Image Template",
				"for_doctype": "ToDo",
				"is_enabled": True,
				"template_html": "test",
			}
		).insert()

		test_template.generate_images_for_existing_documents()
		attached_images = get_attached_images("ToDo", [test_todo_doc.name])
		self.assertIn(test_todo_doc.name, attached_images)
		self.assertEqual(len(attached_images[test_todo_doc.name]), 1)
