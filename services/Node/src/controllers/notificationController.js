const prisma = require("../config/prisma")

const createNotification = async (req, res) => {
    try{
        const {
            userId,
            eventId,
            message,
        } = req.body;
        const notification = await prisma.notification.create({
            data: {
                userId,
                eventId,
                message,
            },
        });
        res.status(201).json(notification);
    } catch (error){
        console.error(error);
        res.status(500).json({
            error: "Failed to create notification",
        });
    }
};

const getNotifications = async (req, res) =>{
    try {
        const notifications = await prisma.notification.findMany({
            orderBy: {
                createdAt: "desc",
            },
        });
        res.json(notifications);
    } catch (error){
        console.error(error);

        res.status(500).json({
            error: "Failed to fetch notifications"
        })
    }
};

module.exports = {
    createNotification,
    getNotifications,
}