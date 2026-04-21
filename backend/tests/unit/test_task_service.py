from api.dependencies import activity_repo, task_service


def test_create_task():
    task = task_service.create_task("Unit Task")
    assert task.title == "Unit Task"
    assert len(activity_repo.store.events) >= 1
