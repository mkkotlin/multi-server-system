const prisma = require("../config/prisma")

const createEvent = async (req, res) => {
    try{
        const {
            eventType,
            source,
            entityType,
            entityId,
            payload,
        } = req.body

        const event = await prisma.event.create({
            data: {
            eventType,
            source,
            entityType,
            entityId,
            payload,
            },
        });
        res.status(201).json(event);
    } catch (error){
        console.error(error)
        res.status(500).json({
            error: "Failed to create event"
        })
    }
};


const getEvents = async (req, res) => {
    try{
        const events = await prisma.event.findMany({
            orderBy:{
                createdAt: "desc",
            },
        });
        res.json(events);
    } catch (error){
        console.error(error);
        res.status(500).json({
            error: "Failed to fetch events",
        });
    }
};

const getEventById = async (req, res) => {
    try{
        const event = await prisma.event.findUnique({
            where:{
                id: req.params.id,
            },
        });
        if (!event){
            return res.status(404).json({
                error: "Event not found",
            });
        }
        res.json(event);
    } catch (error){
        console.error(error);
        res.status(500).json({
            error: "Failed to fetch event",
        })
    };
};


module.exports = {
    createEvent,
    getEvents,
    getEventById
}