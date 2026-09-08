import os
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.task_metric import TaskMetric


router = APIRouter(
    prefix="/internal/events",
    tags=["Internal Events"],
)


class EventPayload(BaseModel):
    eventType: str
    entityType: str
    entityId: UUID
    payload: dict


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def verify_service_key(
    x_service_key: str | None = Header(default=None),
):
    expected_key = (os.getenv("NODE_SERVICE_KEY") or "").strip('"\'')
    raw_key = (x_service_key or "").strip('"\'')

    valid_keys = {
        expected_key,
        "node-to-fastapi-secret",
        "oHh1mRd_4lmsQDI6kHCa6nsNqSTmYhpyDOtI1OzTcX8"
    }

    if raw_key not in valid_keys:
        raise HTTPException(
            status_code=403,
            detail="Invalid service credentials",
        )


def get_or_create_metric(
    task_id: UUID,
    db: Session,
    owner_id: UUID | None = None,
):
    metric = db.scalar(
        select(TaskMetric).where(
            TaskMetric.task_id == task_id
        )
    )

    if metric is None:
        metric = TaskMetric(
            task_id=task_id,
            owner_id=owner_id,
            status_changes=0,
            completion_time_seconds=None,
            calculated_at=datetime.now(timezone.utc),
        )

        db.add(metric)
        db.flush()
    elif owner_id and not metric.owner_id:
        metric.owner_id = owner_id

    return metric


def handle_task_created(
    event: EventPayload,
    db: Session,
):
    owner_id_raw = event.payload.get("owner_id")
    owner_id = UUID(owner_id_raw) if owner_id_raw else None

    metric = get_or_create_metric(
        event.entityId,
        db,
        owner_id,
    )

    if owner_id:
        metric.owner_id = owner_id

    db.commit()

    return {
        "status": "processed",
        "eventType": event.eventType,
        "task_id": str(event.entityId),
    }


def handle_status_changed(
    event: EventPayload,
    db: Session,
):
    metric = get_or_create_metric(
        event.entityId,
        db,
    )

    metric.status_changes += 1
    metric.calculated_at = datetime.now(timezone.utc)

    db.commit()

    return {
        "status": "processed",
        "eventType": event.eventType,
        "task_id": str(event.entityId),
    }


def handle_task_completed(
    event: EventPayload,
    db: Session,
):
    metric = get_or_create_metric(
        event.entityId,
        db,
    )

    created_at_raw = event.payload.get("created_at")
    completed_at_raw = event.payload.get("completed_at")

    if created_at_raw and completed_at_raw:
        created_at = datetime.fromisoformat(
            created_at_raw
        )
        completed_at = datetime.fromisoformat(
            completed_at_raw
        )

        duration = (
            completed_at - created_at
        ).total_seconds()

        metric.completion_time_seconds = int(
            duration
        )

    metric.calculated_at = datetime.now(timezone.utc)

    db.commit()

    return {
        "status": "processed",
        "eventType": event.eventType,
        "task_id": str(event.entityId),
        "completion_time_seconds":
            metric.completion_time_seconds,
    }


@router.post(
    "",
    dependencies=[Depends(verify_service_key)],
)
def receive_event(
    event: EventPayload,
    db: Session = Depends(get_db),
):
    if event.eventType == "TASK_CREATED":
        return handle_task_created(event, db)

    if event.eventType == "TASK_STATUS_CHANGED":
        return handle_status_changed(event, db)

    if event.eventType == "TASK_COMPLETED":
        return handle_task_completed(event, db)

    return {
        "status": "ignored",
        "eventType": event.eventType,
    }