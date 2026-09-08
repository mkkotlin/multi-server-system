from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.metrics import router as metric_router
from app.routes.internal_events import router as internal_events_router

app = FastAPI(title="Triserver Analytics Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metric_router)
app.include_router(internal_events_router)

@app.get("/health")
def health():
    return {"service": "analytics-server", "status": "UP"}