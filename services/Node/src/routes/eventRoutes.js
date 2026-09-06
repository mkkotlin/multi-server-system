const express = require("express")
const authenticate = require("../middleware/auth")
const { createEvent, getEvents, getEventById } = require("../controllers/eventController")

const router = express.Router()
router.use(authenticate)

router.post("/", createEvent);
router.get("/", getEvents);
router.get("/:id", getEventById)

module.exports = router