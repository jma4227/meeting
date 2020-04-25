import frappe


def get_context(context):
	context.planned_meetings = frappe.get_all("Meeting", fields = ["name", "title", "date", "from_time", "to_time"],
											  filters = {"status": "Planned"}, order_by = "date desc")
	
	context.past_meetings = frappe.get_all("Meeting", fields = ["name", "title", "date", "from_time", "to_time"],
										   filters = {"status": "Completed"}, order_by = "date desc",
										   limit_page_length = 20)
