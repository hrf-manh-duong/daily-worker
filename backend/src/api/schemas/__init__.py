from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class UpdateTaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class StartFocusRequest(BaseModel):
    task_id: UUID


class StandupSaveRequest(BaseModel):
    local_date: date
    yesterday: str = Field(default="", max_length=4000)
    today: str = Field(min_length=1, max_length=4000)
    blockers: str = Field(default="", max_length=4000)


class StandupEntryResponse(BaseModel):
    local_date: date
    yesterday: str
    today: str
    blockers: str
    created_at: datetime
    updated_at: datetime


class StandupPrefillResponse(BaseModel):
    for_local_date: date
    source_local_date: date
    completed_tasks: list[str]
    prefill_markdown: str


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
