from datetime import date, datetime, timezone
from typing import Optional
from uuid import UUID

from domain.models import ActivityEvent, FocusSession, StandupEntry, Task


class MemoryStore:
    def __init__(self) -> None:
        self.tasks: dict[UUID, Task] = {}
        self.focus_sessions: dict[UUID, FocusSession] = {}
        self.events: list[ActivityEvent] = []
        self.standup_entries: dict[date, StandupEntry] = {}


class TaskRepository:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def create(self, title: str) -> Task:
        task = Task(title=title.strip())
        self.store.tasks[task.id] = task
        return task

    def update_title(self, task_id: UUID, title: str) -> Optional[Task]:
        task = self.store.tasks.get(task_id)
        if not task:
            return None
        task.title = title.strip()
        task.updated_at = datetime.now(timezone.utc)
        return task

    def complete(self, task_id: UUID) -> Optional[Task]:
        task = self.store.tasks.get(task_id)
        if not task:
            return None
        task.status = "completed"
        task.completed_at = datetime.now(timezone.utc)
        task.updated_at = datetime.now(timezone.utc)
        return task

    def delete(self, task_id: UUID) -> Optional[Task]:
        return self.store.tasks.pop(task_id, None)

    def get(self, task_id: UUID) -> Optional[Task]:
        return self.store.tasks.get(task_id)

    def list(self) -> list[Task]:
        return list(self.store.tasks.values())


class FocusRepository:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def get_active(self) -> Optional[FocusSession]:
        for session in self.store.focus_sessions.values():
            if session.state == "active":
                return session
        return None

    def create(self, task_id: UUID) -> FocusSession:
        session = FocusSession(task_id=task_id)
        self.store.focus_sessions[session.id] = session
        return session

    def stop(self, session: FocusSession, reason: str) -> FocusSession:
        session.state = "ended"
        session.stop_reason = reason
        session.ended_at = datetime.now(timezone.utc)
        return session


class ActivityRepository:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def add(self, event: ActivityEvent) -> ActivityEvent:
        self.store.events.append(event)
        return event

    def list_today(self) -> list[ActivityEvent]:
        day = datetime.now(timezone.utc).date()
        events = [e for e in self.store.events if e.local_day == day]
        priority = {
            "task_created": 1,
            "focus_started": 2,
            "focus_stopped": 3,
            "task_completed": 4,
            "task_updated": 5,
        }
        return sorted(events, key=lambda e: (e.occurred_at, priority.get(e.event_type, 99)))


class StandupRepository:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def upsert(self, entry: StandupEntry) -> StandupEntry:
        existing = self.store.standup_entries.get(entry.local_date)
        if existing is not None:
            entry.created_at = existing.created_at
        entry.updated_at = datetime.now(timezone.utc)
        self.store.standup_entries[entry.local_date] = entry
        return entry

    def get(self, local_date: date) -> Optional[StandupEntry]:
        return self.store.standup_entries.get(local_date)

    def list(self, limit: int) -> list[StandupEntry]:
        entries = sorted(
            self.store.standup_entries.values(),
            key=lambda e: e.local_date,
            reverse=True,
        )
        return entries[:limit]
