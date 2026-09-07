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

const getNotifications = async (req, res) => {
    try {
        const where =
            req.user.role === "ADMIN"
                ? {}
                : {
                    userId: req.user.user_id,
                };

        const notifications = await prisma.notification.findMany({
            where,
            orderBy: {
                createdAt: "desc",
            },
        });

        res.json(notifications);
    } catch (error) {
        console.error(error);

        res.status(500).json({
            error: "Failed to fetch notifications",
        });
    }
};


const markAsRead = async (req, res) =>{
    try{
        const notificationId = req.params.id;
        const user = req.user
        const notification = await prisma.notification.findUnique({
            where:{
                id: notificationId,
            },
        });
        if (!notification){
            return res.status(404).json({
                error: "Notification not found",
            });
        }
        if ( user.role !== "ADMIN" && notification.userId !== user.user_id){
            return res.status(403).json({
                error:"You cannot modify this notification",
            });
        }
        const updateNotification = await prisma.notification.update({
            where:{
                id: notificationId,
            },
            data:{
                isRead: true,
                readAt: new Date(),
            },
        });
        res.json(updateNotification);
    } catch(error){
        console.error(error);
        res.status(500).json({
            error: "Failed to mark notification as rerad",
        });
    }
};


module.exports = {
    createNotification,
    getNotifications,
    markAsRead,
}