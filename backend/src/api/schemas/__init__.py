from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class UpdateTaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class StartFocusRequest(BaseModel):
    task_id: UUID


class TaskResponse(BaseModel):
    id: UUID
    title: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None


class FocusResponse(BaseModel):
    id: UUID
    task_id: UUID
    started_at: datetime
    ended_at: datetime | None = None
    state: str
    stop_reason: str


class EventResponse(BaseModel):
    id: UUID
    event_type: str
    task_id: UUID | None = None
    focus_session_id: UUID | None = None
    occurred_at: datetime
    local_day: date
    payload: dict
