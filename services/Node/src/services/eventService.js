const prisma = require("../config/prisma");

const processEvent = async (event) => {
    switch (event.eventType) {
        case "TASK_CREATED":
            return handleTaskCreated(event);

        case "TASK_COMPLETED":
            return handleTaskCompleted(event);

        case "TASK_REOPENED":
            return handleTaskOpened(event)

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

const handleTaskCompleted = async (event) => {
    const {
        assigned_to,
        title,
    } = event.payload;

    if (!assigned_to) {
        return null;
    }

    return prisma.notification.create({
        data: {
            userId: assigned_to,
            eventId: event.id,
            message: `Task "${title}" was completed.`,
        },
    });
};


const handleTaskOpened = async (event) =>{
    const {
        assigned_to,
        title,
    } = event.payload;

    if (!assigned_to){
        return null;
    }

    return prisma.notification.create({
        data: {
            userId: assigned_to,
            eventId: event.id,
            message: `Task "${title}" was reopened`,
        },
    });
};


module.exports = {
    processEvent,
};