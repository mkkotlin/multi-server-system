const serviceAuth = (req, res, next) =>{
    const serviceKey = req.headers["x-service-key"]

    if (!serviceKey){
        return res.status(401).json({
            error: "Service authentication required"
        });
    }

    if (serviceKey !== process.env.DJANGO_SERVICE_KEY){
        return res.status(403).json({
            error: "Invalid service credentials",
        });
    }

    req.service = "django-service"
    next()
}

module.exports = serviceAuth