from repositories.memory import ActivityRepository, FocusRepository, MemoryStore, TaskRepository
from services.core import FocusService, TaskService, TimelineService

store = MemoryStore()
task_repo = TaskRepository(store)
focus_repo = FocusRepository(store)
activity_repo = ActivityRepository(store)

task_service = TaskService(task_repo, activity_repo)
focus_service = FocusService(task_repo, focus_repo, activity_repo)
timeline_service = TimelineService(activity_repo)
