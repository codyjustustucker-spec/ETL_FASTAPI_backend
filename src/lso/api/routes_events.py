from fastapi import APIRouter, HTTPException, status

from lso.api.schemas import EventsIngestRequest, EventsIngestResponse
from lso.db import queries

router = APIRouter(prefix="/systems", tags=["events"])


@router.post("/{system_id}/events", response_model=EventsIngestResponse, status_code=status.HTTP_202_ACCEPTED)
def ingest_events(system_id: int, payload: EventsIngestRequest) -> EventsIngestResponse:
    if not queries.system_exists(system_id):
        raise HTTPException(status_code=404, detail="System not found")

    inserted = queries.insert_events(
        system_id, [e.model_dump() for e in payload.events])
    return EventsIngestResponse(system_id=system_id, inserted=inserted)
