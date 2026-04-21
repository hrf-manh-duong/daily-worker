from datetime import date, datetime, timezone
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Query

from api.dependencies import standup_service
from api.schemas import (
    StandupEntryResponse,
    StandupPrefillResponse,
    StandupSaveRequest,
)

router = APIRouter(prefix="/standup", tags=["standup"])


def _parse_local_date(header_value: Optional[str]) -> date:
    if header_value is None or header_value.strip() == "":
        return datetime.now(timezone.utc).date()
    try:
        return date.fromisoformat(header_value.strip())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Invalid X-Client-Local-Date") from exc


@router.get("/prefill", response_model=StandupPrefillResponse)
def get_prefill(x_client_local_date: Optional[str] = Header(default=None)):
    for_local_date = _parse_local_date(x_client_local_date)
    return standup_service.get_prefill(for_local_date)


@router.post("", response_model=StandupEntryResponse)
def save_standup(payload: StandupSaveRequest):
    try:
        return standup_service.save(
            payload.local_date,
            payload.yesterday,
            payload.today,
            payload.blockers,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@router.get("", response_model=list[StandupEntryResponse])
def list_standups(limit: int = Query(default=30, ge=1, le=365)):
    return standup_service.list(limit)


@router.get("/{local_date}", response_model=StandupEntryResponse)
def get_standup(local_date: date):
    entry = standup_service.get(local_date)
    if entry is None:
        raise HTTPException(status_code=404, detail="Standup not found")
    return entry
