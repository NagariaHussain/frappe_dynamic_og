# Copyright (c) 2022, Hussain Nagaria and Contributors
# See license.txt

import frappe

from frappe.tests.utils import FrappeTestCase
from frappe_dynamic_og.frappe_dynamic_og.doctype.og_image_template.og_image_template import EnabledTemplateAlreadyExistsException

class TestOGImageCore(FrappeTestCase):
	def test_no_more_than_one_enabled_template_at_a_time(self):
		test_template_1 = frappe.get_doc({
			"doctype": "OG Image Template",
			"for_doctype": "ToDo",
			"is_enabled": True,
			"template_html": "test"
		}).insert()

		test_template_2 = frappe.get_doc({
				"doctype": "OG Image Template",
				"for_doctype": "ToDo",
				"is_enabled": True,
				"template_html": "test2"
			})

		with self.assertRaises(EnabledTemplateAlreadyExistsException):
			test_template_2.insert()

		# Now, disabled the first one
		test_template_1.is_enabled =  False
		test_template_1.save()

		# Second one should save successfully now
		test_template_2.insert()

