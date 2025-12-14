from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from lso.core.windowing import window_bounds
from lso.core.metrics import compute_metrics
from lso.db import queries
from lso.api.schemas import MetricsOut, HealthOut
from lso.core.health import classify_health

router = APIRouter(prefix="/systems", tags=["metrics"])


@router.get("/{system_id}/metrics", response_model=MetricsOut)
def get_metrics(system_id: int, window: int = Query(60, ge=1, le=86400)) -> MetricsOut:
    if not queries.system_exists(system_id):
        raise HTTPException(status_code=404, detail="System not found")

    start_dt, end_dt = window_bounds(window)
    start_iso = start_dt.isoformat()
    end_iso = end_dt.isoformat()

    evs = queries.fetch_events_in_window(system_id, start_iso, end_iso)
    total = len(evs)
    errors = sum(1 for e in evs if e["status"] == "error")
    lats = [int(e["latency_ms"]) for e in evs]

    m = compute_metrics(total=total, errors=errors,
                        latencies_ms=lats, window_seconds=window)

    return MetricsOut(
        system_id=system_id,
        window_seconds=window,
        window_start=start_dt,
        window_end=end_dt,
        total=m["total"],
        errors=m["errors"],
        error_rate=m["error_rate"],
        rps=m["rps"],
        p95_latency=m["p95_latency"],
    )


@router.get("/{system_id}/health", response_model=HealthOut)
def get_health(system_id: int, window: int = Query(300, ge=1, le=86400)) -> HealthOut:
    if not queries.system_exists(system_id):
        raise HTTPException(status_code=404, detail="System not found")

    start_dt, end_dt = window_bounds(window)
    start_iso = start_dt.isoformat()
    end_iso = end_dt.isoformat()

    evs = queries.fetch_events_in_window(system_id, start_iso, end_iso)
    total = len(evs)
    errors = sum(1 for e in evs if e["status"] == "error")
    lats = [int(e["latency_ms"]) for e in evs]

    m = compute_metrics(total=total, errors=errors,
                        latencies_ms=lats, window_seconds=window)
    health, reason = classify_health(m["error_rate"], m["p95_latency"])

    return HealthOut(
        system_id=system_id,
        window_seconds=window,
        window_start=start_dt,
        window_end=end_dt,
        health=health,
        reason=reason,
        total=m["total"],
        errors=m["errors"],
        error_rate=m["error_rate"],
        rps=m["rps"],
        p95_latency=m["p95_latency"],
    )
