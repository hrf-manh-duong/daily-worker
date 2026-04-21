from repositories.memory import (
    ActivityRepository,
    FocusRepository,
    MemoryStore,
    StandupRepository,
    TaskRepository,
)
from services.core import FocusService, StandupService, TaskService, TimelineService

store = MemoryStore()
task_repo = TaskRepository(store)
focus_repo = FocusRepository(store)
activity_repo = ActivityRepository(store)
standup_repo = StandupRepository(store)

task_service = TaskService(task_repo, activity_repo)
focus_service = FocusService(task_repo, focus_repo, activity_repo)
timeline_service = TimelineService(activity_repo)
standup_service = StandupService(standup_repo, task_service)
