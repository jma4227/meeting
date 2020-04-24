# -*- coding: utf-8 -*-
# Copyright (c) 2020, FixationJay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document


# test

class Meeting(Document):
	def validate(self):
		self.validate_attendees()
	
	def on_update(self):
		self.sync_todos()
	
	def validate_attendees(self):
		"""Set missing names and warn if duplicate"""
		found = []
		for attendee in self.attendees:
			if not attendee.full_name:
				attendee.full_name = get_full_name(attendee.attendee)
			
			if attendee.attendee in found:
				frappe.throw(_("Attendee {0} entered twice").format(attendee.attendee))
				
				found.append(attendee.attendee)
	
	def sync_todos(self):
		"""Sync ToDos for assignment"""
		todos_added = [minute.todo for minute in self.minutes if minute.todo]
		
		for minute in self.minutes:
			if minute.assigned_to:
				if not minute.todo:
					todo = frappe.get_doc({
						"doctype": "ToDo",
						"description": minute.description,
						"reference_type": self.doctype,
						"reference_name": self.name,
						"owner": minute.assigned_to
						})
					todo.insert()
					
					minute.db_set("todo", todo.name)


@frappe.whitelist()
def get_full_name(attendee):
	user = frappe.get_doc("User", attendee)
	
	# concantenates by space if it has value
	return " ".join(filter(None, [user.first_name, user.middle_name, user.last_name]))
