from fastapi import APIRouter

from api.dependencies import timeline_service
from api.schemas import EventResponse

router = APIRouter(prefix="/timeline", tags=["timeline"])


@router.get("/today", response_model=list[EventResponse])
def timeline_today():
    return timeline_service.today()
