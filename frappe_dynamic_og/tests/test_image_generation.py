# Copyright (c) 2022, Hussain Nagaria and Contributors
# See license.txt

import frappe

from frappe.tests.utils import FrappeTestCase
from frappe.core.api.file import get_attached_images
from frappe_dynamic_og.core.generate_image import (
	ImageGenerator,
	EnabledTemplateDoesNotExistException,
)
from frappe_dynamic_og.frappe_dynamic_og.doctype.og_image_template.og_image_template import (
	OGImageTemplate,
)


class TestImageGeneration(FrappeTestCase):
	def setUp(self):
		# Disable any existing template
		frappe.db.set_value(
			"OG Image Template", {"is_enabled": True}, "is_enabled", False
		)

		# Create new test template
		self.test_og_template = frappe.get_doc(
			{
				"doctype": "OG Image Template",
				"for_doctype": "ToDo",
				"is_enabled": False,  # enable before using,
				"use_default_template": False,
				"template_html": '<div style="width: 800px; background-color: #ff0000; display: flex;" ><h1>{{ doc.description }}</h1></div>',
			}
		).insert()

	def test_does_not_generate_if_template_disabled(self):
		test_todo_doc = frappe.get_doc(
			{"doctype": "ToDo", "description": "Hello, Hussain!"}
		).insert()

		attached_images = get_attached_images("ToDo", [test_todo_doc.name])
		self.assertEqual(len(attached_images), 0)

	def test_image_attached_if_template_enabled(self):
		# enable the test template
		self.test_og_template.is_enabled = True
		self.test_og_template.save()

		# create a new todo doc
		test_todo_doc = frappe.get_doc(
			{"doctype": "ToDo", "description": "Bro, what's up?"}
		).insert()

		attached_images = get_attached_images("ToDo", [test_todo_doc.name])
		self.assertEqual(len(attached_images), 1)
		self.assertTrue(
			attached_images[test_todo_doc.name][0].startswith("/files/og_image_todo_")
		)

	def test_deletes_older_images_if_applicable(self):
		# enable the test template
		self.test_og_template.is_enabled = True
		self.test_og_template.save()

		frappe_og_settings = frappe.get_single("Frappe Dynamic OG Settings")

		# Turn Off automatic deletion
		frappe_og_settings.automatically_delete_old_images = False
		frappe_og_settings.save()
		
		test_todo_doc = frappe.get_doc(
			{"doctype": "ToDo", "description": "Hello, Hussain!"}
		).insert()

		attached_images = get_attached_images("ToDo", [test_todo_doc.name])
		self.assertEqual(len(attached_images[test_todo_doc.name]), 1)

		# Update the document
		test_todo_doc.description = "Wednesday Addams"
		test_todo_doc.save()

		# 2 images should be present
		attached_images = get_attached_images("ToDo", [test_todo_doc.name])
		self.assertEqual(len(attached_images[test_todo_doc.name]), 2)

		# Turn on automatic deletion
		frappe_og_settings.automatically_delete_old_images = True
		frappe_og_settings.save()
		
		# Create a new one
		test_todo_doc.description = "Sheldon, Raj, Howard and Leonard are my bros!"
		test_todo_doc.save()

		# Only the latest image must be attached (the other 2 get deleted)
		attached_images = get_attached_images("ToDo", [test_todo_doc.name])
		self.assertEqual(len(attached_images[test_todo_doc.name]), 1)

	def test_image_attached_to_field_if_applicable(self):
		frappe.get_doc(
			{
				"doctype": "OG Image Template",
				"for_doctype": "User",
				"is_enabled": True,
				"template_html": '<div style="width: 800px; background-color: #00ffe9; display: flex;" ><h1>{{ doc.username }}</h1></div>',
				"attach_to_image_field": True,
				"image_field": "banner_image",
			}
		).insert()

		# Remove if already exists, when in local
		if frappe.db.exists("User", {"name": "wednesday.addams@netflix.com"}):
			frappe.delete_doc("User", "wednesday.addams@netflix.com")

		test_user_doc = frappe.get_doc(
			{
				"doctype": "User",
				"first_name": "Wednesday",
				"last_name": "Addams",
				"send_welcome_email": False,
				"email": "wednesday.addams@netflix.com",
			}
		).insert()

		attached_images = get_attached_images("User", [test_user_doc.name])
		attached_images = attached_images[test_user_doc.name]
		self.assertEqual(len(attached_images), 1)

		test_user_doc.reload()
		self.assertEqual(test_user_doc.banner_image, attached_images[0])

	def test_should_throw_if_enabled_template_does_not_exist(self):
		self.test_document = frappe.get_doc(
			{"doctype": "Web Page", "title": "Test Web Page Title"}
		).insert()

		with self.assertRaises(EnabledTemplateDoesNotExistException):
			generator = ImageGenerator(self.test_document)

	def test_supports_img_embedding(self):
		test_template: OGImageTemplate = frappe.get_doc(
			{
				"doctype": "OG Image Template",
				"for_doctype": "ToDo",
				"is_enabled": True,
				"template_html": '<div style="display: flex;"><img src="https://frappe.io/files/frappe.png" /><h1>Hello</h1></div>',
			}
		).insert()

		image_generator = ImageGenerator(test_template, is_preview=True)
		file_doc = image_generator.generate()
		self.assertIsNotNone(file_doc)

	def test_template_html_required_for_custom_template(self):
		# enable the test template
		self.test_og_template.is_enabled = True
		self.test_og_template.template_html = ""

		with self.assertRaises(frappe.ValidationError):
			self.test_og_template.save()

	def test_uses_default_template(self):
		# enable the test template
		self.test_og_template.is_enabled = True
		self.test_og_template.template_html = ""
		self.test_og_template.use_default_template = True
		self.test_og_template.save()

		image_generator = ImageGenerator(self.test_og_template, is_preview=True)
		file_doc = image_generator.generate()
		self.assertIsNotNone(file_doc)




	def tearDown(self):
		# Clean up docs
		if hasattr(self, "test_document"):
			self.test_document.delete()
