from uuid import UUID
from fastapi import APIRouter, HTTPException, Response

from api.dependencies import focus_service, task_service
from api.schemas import CreateTaskRequest, TaskResponse, UpdateTaskRequest

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(payload: CreateTaskRequest):
    try:
        return task_service.create_task(payload.title)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid title")


@router.get("", response_model=list[TaskResponse])
def list_tasks():
    return task_service.list_tasks()


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: UUID, payload: UpdateTaskRequest):
    try:
        return task_service.update_task(task_id, payload.title)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid title")


@router.post("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: UUID):
    try:
        return task_service.complete_task(task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: UUID):
    active = focus_service.focus.get_active()
    if active is not None and active.task_id == task_id:
        focus_service.stop_focus("manual")
    try:
        task_service.delete_task(task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=204)
