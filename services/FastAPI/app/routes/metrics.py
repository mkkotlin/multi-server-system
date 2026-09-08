from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.task_metric import TaskMetric
from app.schemas.task_metric import TicketMetricResponse, MetricsSummaryResponse
from app.auth import get_current_user

router = APIRouter(
    prefix="/api/metrics",
    tags=["Metrics"],
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/summary",
    response_model=MetricsSummaryResponse,
)
def get_metrics_summary(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    query = select(TaskMetric)

    if user.get("role") != "ADMIN":
        user_id_str = user.get("user_id")
        user_uuid = UUID(user_id_str) if user_id_str else None
        query = query.where(
            TaskMetric.owner_id == user_uuid
        )

    metrics = db.scalars(query).all()

    total_tasks = len(metrics)

    completed_tasks = sum(
        1
        for metric in metrics
        if metric.completion_time_seconds is not None
    )

    completion_times = [
        metric.completion_time_seconds
        for metric in metrics
        if metric.completion_time_seconds is not None
    ]

    average_completion_time = (
        sum(completion_times) / len(completion_times)
        if completion_times
        else None
    )

    total_status_changes = sum(
        metric.status_changes
        for metric in metrics
    )

    return MetricsSummaryResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        average_completion_time_seconds=average_completion_time,
        total_status_changes=total_status_changes,
    )

@router.get(
    "/tasks/{task_id}",
    response_model=TicketMetricResponse,
)
def get_task_metric(
    task_id: UUID,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    metric = db.scalar(
        select(TaskMetric).where(
            TaskMetric.task_id == task_id
        )
    )

    if metric is None:
        raise HTTPException(
            status_code=404,
            detail="Metrics not found",
        )

    if user.get("role") != "ADMIN":
        if metric.owner_id and str(metric.owner_id) != str(user.get("user_id")):
            raise HTTPException(
                status_code=403,
                detail="You cannot access these metrics",
            )

    return metric