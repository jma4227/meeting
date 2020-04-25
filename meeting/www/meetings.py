import frappe


def get_context(context):
	context.planned_meetings = get_meetings("Planned")
	
	context.past_meetings = get_meetings("Completed", limit_page_length = 20)


def get_meetings(status, **kwargs):
	return frappe.get_all("Meeting", fields = ["name", "title", "date", "from_time", "to_time"],
						  filters = {"status": "Completed", "show_in_website": 1},
						  order_by = "date desc", **kwargs)
