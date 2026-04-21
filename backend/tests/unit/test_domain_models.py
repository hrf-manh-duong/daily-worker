from domain.models import ActivityEvent, FocusSession, Task


def test_domain_models_construct():
    task = Task(title="a")
    session = FocusSession(task_id=task.id)
    event = ActivityEvent(event_type="task_created", task_id=task.id)
    assert task.id is not None
    assert session.task_id == task.id
    assert event.task_id == task.id
