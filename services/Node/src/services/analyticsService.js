const axios = require("axios");

const sendEventToAnalytics = async (event) => {
	try {
		const response = await axios.post(
			`${process.env.FASTAPI_ANALYTICS_URL || "http://localhost:8002"}/internal/events`,
			{
				eventType: event.eventType,
				entityType: event.entityType,
				entityId: event.entityId,
				eventId: event.entityId,
				payload: typeof event.payload === 'string' ? JSON.parse(event.payload) : event.payload,
			},
			{
				headers: {
					"X-Service-Key": process.env.FASTAPI_SERVICE_KEY || "oHh1mRd_4lmsQDI6kHCa6nsNqSTmYhpyDOtI1OzTcX8",
				},
				timeout: 5000,
			}
		);
		console.log("Analytics response:", response.data);
		return response.data;
	} catch (error) {
		console.error("Failed to send event to analytics:", error.message, error.response ? JSON.stringify(error.response.data) : "");
		return null;
	}
};

module.exports = {
	sendEventToAnalytics
};