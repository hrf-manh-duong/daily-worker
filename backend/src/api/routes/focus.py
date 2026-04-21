from fastapi import APIRouter, HTTPException

from api.dependencies import focus_service
from api.schemas import FocusResponse, StartFocusRequest

router = APIRouter(prefix="/focus", tags=["focus"])


@router.post("/start", response_model=FocusResponse, status_code=201)
def start_focus(payload: StartFocusRequest):
    try:
        return focus_service.start_focus(payload.task_id)
    except RuntimeError:
        raise HTTPException(status_code=409, detail="Active session already exists")
    except ValueError:
        raise HTTPException(status_code=400, detail="Task invalid for focus")


@router.post("/stop", response_model=FocusResponse)
def stop_focus():
    try:
        return focus_service.stop_focus("manual")
    except RuntimeError:
        raise HTTPException(status_code=409, detail="No active session")
