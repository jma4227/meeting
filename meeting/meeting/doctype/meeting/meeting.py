# -*- coding: utf-8 -*-
# Copyright (c) 2020, FixationJay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.website.website_generator import WebsiteGenerator


class Meeting(WebsiteGenerator):
	website = frappe._dict(
		template = "templates/generators/meeting.html",
	
	)
	
	def validate(self):
		self.page_name = self.name.lower()
		
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
		todos_added = [todo.name for todo in
					   frappe.get_all("ToDo",
									  filters = {
										  "reference_type": self.doctype,
										  "reference_name": self.name,
										  "assigned_by"   : ""
									  })
					   ]
		
		# loop through child table minutes
		for minute in self.minutes:
			# check if minute is assigned to user, and  is in open status
			if minute.assigned_to and minute.status == "Open":
				# adds todo to open minute if it doesn't exist
				if not minute.todo:
					todo = frappe.get_doc({
						"doctype"       : "ToDo",
						"description"   : minute.description,
						"reference_type": self.doctype,
						"reference_name": self.name,
						"owner"         : minute.assigned_to
					})
					todo.insert()
					# set value in the database for
					minute.db_set("todo", todo.name, update_modified = False)
				
				#  removes todo from associated minute if todo is deleted
				else:
					todos_added.remove(minute.todo)
			else:
				minute.db_set("todo", None, update_modified = False)
		
		for todo in todos_added:
			# remove closed or old todos
			todo = frappe.get_doc("ToDo", todo)
			todo.flags.from_meeting = True
			todo.delete()


@frappe.whitelist()
def get_full_name(attendee):
	user = frappe.get_doc("User", attendee)
	
	# concantenates by space if it has value
	return " ".join(filter(None, [user.first_name, user.middle_name, user.last_name]))
