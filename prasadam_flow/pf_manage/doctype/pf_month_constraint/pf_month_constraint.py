# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from hkm.utils import validate_child_single_field_duplicacy


class PFMonthConstraint(Document):
	def validate(self):
		validate_child_single_field_duplicacy(self, "constraints", "coupon_category")
		return

	def on_update(self):
		self.delete_cache_month_key()
		self.delete_cache_custodian_group_key()

	def on_trash(self):
		self.delete_cache_month_key()
		self.delete_cache_custodian_group_key()

	def delete_cache_month_key(self):
		frappe.cache().hdel("pf_month_constraint", self.constraint_month)

	def delete_cache_custodian_group_key(self):
		frappe.cache().hdel("pf_month_constraint", self.custodian_group)
