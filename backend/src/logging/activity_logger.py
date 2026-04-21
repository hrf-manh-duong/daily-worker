import logging
from domain.models import ActivityEvent

logger = logging.getLogger("daily_worker.activity")


def log_activity(event: ActivityEvent) -> None:
    logger.info(
        "activity_event",
        extra={
            "event_type": event.event_type,
            "task_id": str(event.task_id) if event.task_id else None,
            "focus_session_id": str(event.focus_session_id) if event.focus_session_id else None,
            "occurred_at": event.occurred_at.isoformat(),
        },
    )
