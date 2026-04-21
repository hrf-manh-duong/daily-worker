from datetime import datetime
from domain.models import ActivityEvent
from app_logging.activity_logger import log_activity


def test_activity_logger_runs():
    event = ActivityEvent(event_type="task_created", occurred_at=datetime.utcnow())
    log_activity(event)
