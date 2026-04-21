from api.dependencies import focus_service, task_service


def test_focus_lifecycle():
    task = task_service.create_task("Focus Unit")
    session = focus_service.start_focus(task.id)
    assert session.state == "active"
    stopped = focus_service.stop_focus()
    assert stopped.state == "ended"
