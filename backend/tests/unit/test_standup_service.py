from datetime import date, datetime, timedelta, timezone

import pytest

from domain.models import Task
from repositories.memory import (
    ActivityRepository,
    MemoryStore,
    StandupRepository,
    TaskRepository,
)
from services.core import StandupService, TaskService


@pytest.fixture
def store() -> MemoryStore:
    return MemoryStore()


@pytest.fixture
def services(store):
    tasks = TaskRepository(store)
    events = ActivityRepository(store)
    standups = StandupRepository(store)
    task_service = TaskService(tasks, events)
    return StandupService(standups, task_service), task_service, store


def test_save_requires_non_empty_today(services):
    standup, _, _ = services
    with pytest.raises(ValueError, match="invalid_today"):
        standup.save(date(2026, 4, 21), "y", "   ", "b")


def test_save_trims_fields(services):
    standup, _, _ = services
    entry = standup.save(date(2026, 4, 21), "  y  ", "  t  ", "  b  ")
    assert entry.yesterday == "y"
    assert entry.today == "t"
    assert entry.blockers == "b"


def test_save_rejects_oversized_field(services):
    standup, _, _ = services
    big = "x" * 4001
    with pytest.raises(ValueError, match="field_too_long"):
        standup.save(date(2026, 4, 21), big, "ok", "")


def test_save_overwrite_preserves_created_at(services):
    standup, _, _ = services
    local = date(2026, 4, 21)
    first = standup.save(local, "y1", "t1", "")
    second = standup.save(local, "y2", "t2", "b2")
    assert first.created_at == second.created_at
    assert second.updated_at >= first.updated_at
    assert second.yesterday == "y2" and second.today == "t2" and second.blockers == "b2"


def test_list_sorted_newest_first_and_capped(services):
    standup, _, _ = services
    for i in range(5):
        standup.save(date(2026, 4, 10 + i), "", f"day {i}", "")
    result = standup.list(limit=3)
    assert [e.local_date for e in result] == [date(2026, 4, 14), date(2026, 4, 13), date(2026, 4, 12)]


def test_list_limit_clamped(services):
    standup, _, _ = services
    standup.save(date(2026, 4, 21), "", "t", "")
    assert len(standup.list(limit=0)) == 1  # clamped to min 1
    assert len(standup.list(limit=10_000)) == 1  # still returns what's there


def test_get_returns_none_for_missing(services):
    standup, _, _ = services
    assert standup.get(date(2026, 4, 21)) is None


def test_prefill_uses_previous_day_completed_tasks(services, store):
    standup, task_service, _ = services
    yesterday = date(2026, 4, 20)
    today = date(2026, 4, 21)
    # Task completed yesterday at 10:00 UTC
    task1 = task_service.create_task("Completed yesterday early")
    task2 = task_service.create_task("Completed yesterday late")
    task3 = task_service.create_task("Still active")
    task_service.complete_task(task1.id)
    task_service.complete_task(task2.id)
    # Move completed_at back to yesterday
    store.tasks[task1.id].completed_at = datetime.combine(yesterday, datetime.min.time(), tzinfo=timezone.utc) + timedelta(hours=9)
    store.tasks[task2.id].completed_at = datetime.combine(yesterday, datetime.min.time(), tzinfo=timezone.utc) + timedelta(hours=17)

    prefill = standup.get_prefill(today)
    assert prefill["for_local_date"] == today
    assert prefill["source_local_date"] == yesterday
    assert prefill["completed_tasks"] == [
        "Completed yesterday early",
        "Completed yesterday late",
    ]
    assert prefill["prefill_markdown"] == "- Completed yesterday early\n- Completed yesterday late"
    # Active task not included
    assert task3.title not in prefill["completed_tasks"]


def test_prefill_empty_when_nothing_completed_yesterday(services):
    standup, _, _ = services
    prefill = standup.get_prefill(date(2026, 4, 21))
    assert prefill["completed_tasks"] == []
    assert prefill["prefill_markdown"] == ""


def test_prefill_excludes_tasks_completed_today(services, store):
    standup, task_service, _ = services
    today = date(2026, 4, 21)
    task = task_service.create_task("Done today")
    task_service.complete_task(task.id)
    store.tasks[task.id].completed_at = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc) + timedelta(hours=8)
    prefill = standup.get_prefill(today)
    assert prefill["completed_tasks"] == []


def test_prefill_read_only_does_not_mutate_tasks(services, store):
    standup, task_service, _ = services
    task_service.create_task("A")
    original_events = list(store.events)
    standup.get_prefill(date(2026, 4, 21))
    assert store.events == original_events
