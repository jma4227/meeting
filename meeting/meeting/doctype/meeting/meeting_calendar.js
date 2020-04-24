
frappe.views.calendar["Meeting"] = {
	field_map: {
		"start": "start",
		"end": "end",
		"id": "name",
		"title": "title",
		"status" : "status",
	},
	// options: {
	// 	header: {
	// 		left: 'prev,next today',
	// 		center: 'title',
	// 		right: 'month'
	// 	}
	// },
	get_events_method: "meeting.api.get_meetings"
}