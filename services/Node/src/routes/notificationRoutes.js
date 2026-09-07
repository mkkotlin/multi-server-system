const express = require("express")
const authenticate = require("../middleware/auth")
const { createNotification, getNotifications, markAsRead } = require("../controllers/notificationController")

const router = express.Router();
router.use(authenticate)

router.post("/", createNotification)
router.get("/", getNotifications)
router.patch("/:id/read", markAsRead)

module.exports = router;