const express = require("express")
const eventRoutes = require("./routes/eventRoutes")
const notificationRoutes = require("./routes/notificationRoutes")
const cors = require("cors")
require("dotenv").config();
const prisma = require("./config/prisma")
const app = express()

app.use(cors())
app.use(express.json())

app.get("/health", (req, res) => {
    res.json({
        service: "event-server",
        status: "UP",
    })
});
app.get("/health/db", async (req, res) => {
    try {
        await prisma.$queryRaw`SELECT 1`;
        res.json({
            service: "event-server",
            database: "UP",
        })
    } catch (error) {
        console.error(error)
        res.status(500).json({
            service: "event-server",
            database: "DOWN",
        })
    }
})

app.use("/api/events", eventRoutes);
app.use("/api/notifications", notificationRoutes)
const PORT = process.env.PORT || 8001

app.listen(PORT, () => {
    console.log(`Event Server running on port ${PORT}`)
})
