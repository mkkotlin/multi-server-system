const express = require("express")
const cors = require("cors")
require("dotenv").config();
const pool = require("./config/db")
const app = express()

app.use(cors())
app.use(express.json())

app.get("/health", (req, res) => {
    res.json({
        service: "event-server",
        status: "UP",
    })
});
app.get("/health/db", async (req, res)=> {
    try{
        const result = await pool.query("SELECT NOW()")
        res.json({
            service: "event-server",
            database: "UP",
            time: result.rows[0].now,
        })
    } catch(error){
        console.error(error)
        res.status(500).json({
            service: "event-server",
            database: "DOWN",
        })
    }
})

const PORT = process.env.PORT || 8001

app.listen(PORT, () => {
    console.log(`Event Server running on port ${PORT}`)
})
