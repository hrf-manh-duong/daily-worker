from repositories.memory import ActivityRepository, FocusRepository, MemoryStore, TaskRepository


def test_repositories_smoke():
    store = MemoryStore()
    tasks = TaskRepository(store)
    focus = FocusRepository(store)
    events = ActivityRepository(store)
    task = tasks.create("Repo test")
    session = focus.create(task.id)
    assert tasks.get(task.id) is not None
    assert focus.get_active() == session
    assert events.list_today() == []
