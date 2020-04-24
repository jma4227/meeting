# -*- coding: utf-8 -*-
# Copyright (c) 2020, FixationJay and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document


class Meeting(Document):
	def validate(self):
		"""Set missing names"""
		for attendee in self.attendees:
			if not attendee.full_name:
				user = frappe.get_doc("User", attendee.attendee)
				# concantenates by space if it has value
				attendee.full_name = " ".join(filter(None, [user.first_name, user.middle_name, user.last_name]))
