const express = require("express")
const authenticate = require("../middleware/auth")
const { createNotification, getNotifications } = require("../controllers/notificationController")

const router = express.Router();
router.use(authenticate)

router.post("/", createNotification)
router.get("/", getNotifications)

module.exports = router;