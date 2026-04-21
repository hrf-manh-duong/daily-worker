from datetime import datetime
from uuid import UUID

from domain.models import ActivityEvent
from app_logging.activity_logger import log_activity
from repositories.memory import ActivityRepository, FocusRepository, TaskRepository


class TaskService:
    def __init__(self, tasks: TaskRepository, events: ActivityRepository) -> None:
        self.tasks = tasks
        self.events = events

    def create_task(self, title: str):
        if not title.strip() or len(title.strip()) > 200:
            raise ValueError("invalid_title")
        task = self.tasks.create(title)
        event = ActivityEvent(event_type="task_created", task_id=task.id, payload={"title": task.title})
        self.events.add(event)
        log_activity(event)
        return task

    def update_task(self, task_id: UUID, title: str):
        if not title.strip() or len(title.strip()) > 200:
            raise ValueError("invalid_title")
        task = self.tasks.update_title(task_id, title)
        if task is None:
            raise KeyError("task_not_found")
        event = ActivityEvent(event_type="task_updated", task_id=task.id, payload={"title": task.title})
        self.events.add(event)
        log_activity(event)
        return task

    def complete_task(self, task_id: UUID):
        task = self.tasks.complete(task_id)
        if task is None:
            raise KeyError("task_not_found")
        event = ActivityEvent(event_type="task_completed", task_id=task.id)
        self.events.add(event)
        log_activity(event)
        return task

    def list_tasks(self):
        return self.tasks.list()

    def delete_task(self, task_id: UUID):
        task = self.tasks.delete(task_id)
        if task is None:
            raise KeyError("task_not_found")
        event = ActivityEvent(event_type="task_deleted", task_id=task.id, payload={"title": task.title})
        self.events.add(event)
        log_activity(event)
        return task


class FocusService:
    def __init__(self, tasks: TaskRepository, focus: FocusRepository, events: ActivityRepository) -> None:
        self.tasks = tasks
        self.focus = focus
        self.events = events

    def start_focus(self, task_id: UUID):
        if self.focus.get_active() is not None:
            raise RuntimeError("focus_already_active")
        task = self.tasks.get(task_id)
        if task is None or task.status == "completed":
            raise ValueError("invalid_task")
        session = self.focus.create(task_id)
        event = ActivityEvent(event_type="focus_started", task_id=task_id, focus_session_id=session.id)
        self.events.add(event)
        log_activity(event)
        return session

    def stop_focus(self, reason: str = "manual"):
        active = self.focus.get_active()
        if active is None:
            raise RuntimeError("no_active_focus")
        session = self.focus.stop(active, reason)
        event = ActivityEvent(event_type="focus_stopped", task_id=session.task_id, focus_session_id=session.id)
        self.events.add(event)
        log_activity(event)
        return session

    def rollover_stop(self):
        active = self.focus.get_active()
        if active and datetime.utcnow().time().hour == 23:
            return self.stop_focus("day_rollover")
        return None


class TimelineService:
    def __init__(self, events: ActivityRepository) -> None:
        self.events = events

    def today(self):
        return self.events.list_today()
