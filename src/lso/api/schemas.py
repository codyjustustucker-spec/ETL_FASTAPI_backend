from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Any
from typing import Optional


class SystemCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class SystemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    created_at: datetime


class EventStatus(str, Enum):
    ok = "ok"
    error = "error"


class EventIn(BaseModel):
    ts: datetime
    event_type: str = Field(min_length=1, max_length=100)
    status: EventStatus
    latency_ms: int = Field(ge=0, le=60_000)
    payload: dict[str, Any] = Field(default_factory=dict)


class EventsIngestRequest(BaseModel):
    events: list[EventIn] = Field(min_length=1, max_length=10_000)


class EventsIngestResponse(BaseModel):
    system_id: int
    inserted: int


class MetricsOut(BaseModel):
    system_id: int
    window_seconds: int
    window_start: datetime
    window_end: datetime
    total: int
    errors: int
    error_rate: float
    rps: float
    p95_latency: Optional[float] = None


class HealthOut(BaseModel):
    system_id: int
    window_seconds: int
    window_start: datetime
    window_end: datetime

    health: str
    reason: str

    total: int
    errors: int
    error_rate: float
    rps: float
    p95_latency: Optional[float] = None
