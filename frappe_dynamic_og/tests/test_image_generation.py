# Copyright (c) 2022, Hussain Nagaria and Contributors
# See license.txt

import frappe

from frappe.tests.utils import FrappeTestCase
from frappe.core.api.file import get_attached_images
import unittest


class TestImageGeneration(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		# Disable any existing template
		frappe.db.set_value(
			"OG Image Template", {"is_enabled": True}, "is_enabled", False
		)

		# Create new test template
		cls.test_og_template = frappe.get_doc(
			{
				"doctype": "OG Image Template",
				"for_doctype": "ToDo",
				"is_enabled": False,  # enable before using,
				"template_html": '<div style="width: 800px; background-color: #ff0000; display: flex;" ><h1>{{ doc.description }}</h1></div>',
			}
		)

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
