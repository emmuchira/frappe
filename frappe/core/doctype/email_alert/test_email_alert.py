# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# See license.txt

import frappe, frappe.utils, frappe.utils.scheduler
import unittest

test_records = frappe.get_test_records('Email Alert')

class TestEmailAlert(unittest.TestCase):
	def setUp(self):
		frappe.db.sql("""delete from `tabBulk Email`""")

	def test_new_and_save(self):
		frappe.set_user("test1@example.com")
		comment = frappe.new_doc("Comment")
		comment.comment = "test"
		comment.insert(ignore_permissions=True)

		self.assertTrue(frappe.db.get_value("Bulk Email", {"ref_doctype": "Comment",
			"ref_docname": comment.name, "status":"Not Sent"}))

		frappe.db.sql("""delete from `tabBulk Email`""")

		comment.description = "test"
		comment.save()

		self.assertTrue(frappe.db.get_value("Bulk Email", {"ref_doctype": "Comment",
			"ref_docname": comment.name, "status":"Not Sent"}))

	def test_condition(self):
		frappe.set_user("test1@example.com")
		event = frappe.new_doc("Event")
		event.subject = "test",
		event.event_type = "Private"
		event.starts_on  = "2014-06-06 12:00:00"
		event.insert()

		self.assertFalse(frappe.db.get_value("Bulk Email", {"ref_doctype": "Event",
			"ref_docname": event.name, "status":"Not Sent"}))

		event.event_type = "Public"
		event.save()

		self.assertTrue(frappe.db.get_value("Bulk Email", {"ref_doctype": "Event",
			"ref_docname": event.name, "status":"Not Sent"}))

	def test_value_changed(self):
		frappe.set_user("test1@example.com")
		event = frappe.new_doc("Event")
		event.subject = "test",
		event.event_type = "Private"
		event.starts_on  = "2014-06-06 12:00:00"
		event.insert()

		self.assertFalse(frappe.db.get_value("Bulk Email", {"ref_doctype": "Event",
			"ref_docname": event.name, "status":"Not Sent"}))

		event.subject = "test 1"
		event.save()

		self.assertFalse(frappe.db.get_value("Bulk Email", {"ref_doctype": "Event",
			"ref_docname": event.name, "status":"Not Sent"}))

		event.description = "test"
		event.save()

		self.assertTrue(frappe.db.get_value("Bulk Email", {"ref_doctype": "Event",
			"ref_docname": event.name, "status":"Not Sent"}))

	def test_date_changed(self):
		frappe.set_user("test1@example.com")
		event = frappe.new_doc("Event")
		event.subject = "test",
		event.event_type = "Private"
		event.starts_on = "2014-01-01 12:00:00"
		event.insert()

		self.assertFalse(frappe.db.get_value("Bulk Email", {"ref_doctype": "Event",
			"ref_docname": event.name, "status":"Not Sent"}))

		frappe.utils.scheduler.trigger(frappe.local.site, "daily", now=True)

		# not today, so no alert
		self.assertFalse(frappe.db.get_value("Bulk Email", {"ref_doctype": "Event",
			"ref_docname": event.name, "status":"Not Sent"}))

		event.starts_on  = frappe.utils.add_days(frappe.utils.nowdate(), 2) + " 12:00:00"
		event.save()

		self.assertFalse(frappe.db.get_value("Bulk Email", {"ref_doctype": "Event",
			"ref_docname": event.name, "status":"Not Sent"}))

		frappe.utils.scheduler.trigger(frappe.local.site, "daily", now=True)

		# today so show alert
		self.assertTrue(frappe.db.get_value("Bulk Email", {"ref_doctype": "Event",
			"ref_docname": event.name, "status":"Not Sent"}))
