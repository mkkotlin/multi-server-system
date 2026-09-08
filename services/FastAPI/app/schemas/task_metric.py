from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class TicketMetricResponse(BaseModel):
    id: UUID
    task_id: UUID
    owner_id: UUID | None = None
    created_at: datetime | None = None
    completion_time_seconds: int | None = None
    status_changes: int
    calculated_at: datetime

    model_config = {
        "from_attributes": True
    }


class MetricsSummaryResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    average_completion_time_seconds: float | None
    total_status_changes: int