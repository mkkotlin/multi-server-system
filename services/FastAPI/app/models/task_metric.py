import uuid
from datetime import datetime
from sqlalchemy import DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class TaskMetric(Base):
	__tablename__ = "task_metrics"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
	owner_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
	created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
	completion_time_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
	status_changes: Mapped[int] = mapped_column(Integer, default=0)
	calculated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)