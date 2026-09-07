const express = require("express")
const serviceAuth = require("../middleware/serviceAuth")

const { createEvent } = require("../controllers/eventController")

const router = express.Router()

router.use(serviceAuth)
router.post("/", createEvent)

module.exports = router