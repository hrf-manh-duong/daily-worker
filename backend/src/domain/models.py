from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from typing import Optional
from uuid import UUID, uuid4


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Task:
    title: str
    id: UUID = field(default_factory=uuid4)
    status: str = "active"
    created_at: datetime = field(default_factory=_now)
    completed_at: Optional[datetime] = None
    updated_at: datetime = field(default_factory=_now)


@dataclass
class FocusSession:
    task_id: UUID
    id: UUID = field(default_factory=uuid4)
    started_at: datetime = field(default_factory=_now)
    ended_at: Optional[datetime] = None
    state: str = "active"
    stop_reason: str = "manual"


@dataclass
class ActivityEvent:
    event_type: str
    task_id: Optional[UUID] = None
    focus_session_id: Optional[UUID] = None
    occurred_at: datetime = field(default_factory=_now)
    local_day: date = field(default_factory=lambda: _now().date())
    id: UUID = field(default_factory=uuid4)
    payload: dict = field(default_factory=dict)


@dataclass
class StandupEntry:
    local_date: date
    yesterday: str = ""
    today: str = ""
    blockers: str = ""
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)
