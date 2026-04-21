import logging
from domain.models import ActivityEvent

logger = logging.getLogger("daily_worker.activity")


def log_activity(event: ActivityEvent) -> None:
    logger.info(
        "activity_event type=%s task=%s focus=%s at=%s",
        event.event_type,
        str(event.task_id) if event.task_id else "-",
        str(event.focus_session_id) if event.focus_session_id else "-",
        event.occurred_at.isoformat(),
    )
