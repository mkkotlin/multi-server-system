const prisma = require("../config/prisma");

const processEvent = async (event) => {
    switch (event.eventType) {
        case "TASK_CREATED":
            return handleTaskCreated(event);

        default:
            console.log(
                `No handler for event type: ${event.eventType}`
            );

            return null;
    }
};

const handleTaskCreated = async (event) => {
    const {
        assigned_to,
        created_by,
        title,
    } = event.payload;

    const userId = assigned_to || created_by;

    if (!userId) {
        return null;
    }

    return prisma.notification.create({
        data: {
            userId,
            eventId: event.id,
            message: `Task "${title}" was created.`,
        },
    });
};

module.exports = {
    processEvent,
};