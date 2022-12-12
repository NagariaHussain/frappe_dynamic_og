# Copyright (c) 2022, Hussain Nagaria and Contributors
# See license.txt

import frappe

from frappe.tests.utils import FrappeTestCase
from frappe_dynamic_og.frappe_dynamic_og.doctype.og_image_template.og_image_template import (
	EnabledTemplateAlreadyExistsException,
	OGImageTemplate,
)


class TestOGImageCore(FrappeTestCase):
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
		self.assertIsNotNone(test_template.preview_image_file)
		self.assertIsInstance(test_template.preview_image_file, str)

		# the image should be private
		file_is_private = frappe.db.get_value(
			"File",
			{
				"file_url": "/private/files/og_image_og_image_template_46f1a39981_bec29990.png"
			},
			"is_private",
		)
		self.assertTrue(file_is_private)
