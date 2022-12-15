# Copyright (c) 2022, Hussain Nagaria and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe_dynamic_og.core.generate_image import get_frappe_og_settings


class FrappeDynamicOGSettings(Document):
    def on_update(self):
        get_frappe_og_settings.clear_cache()
