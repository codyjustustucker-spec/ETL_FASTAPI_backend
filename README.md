# LSO Backend – Telemetry & Health Service

## Overview

This repository contains the **LSO (Living Systems Observatory) backend**, a FastAPI-based service responsible for **receiving telemetry events from ETL systems**, storing them, and computing **system health metrics** over a rolling time window.

The backend is intentionally lightweight and focused:

* It does **not** run ETL jobs
* It does **not** control data pipelines
* It **observes** systems by ingesting structured events

Multiple ETL pipelines can report into a single backend instance.

---

## Core Responsibilities

* Accept telemetry events from external systems
* Validate event schemas
* Persist events
* Aggregate recent events per system
* Expose health summaries via an API

This separation allows ETL systems to remain simple while still being observable.

---

## Architecture

**High-level flow:**

```
ETL Pipeline(s)
      ↓
POST /systems/{system_id}/events
      ↓
Event Store (DB / in-memory)
      ↓
Health Aggregator
      ↓
GET /systems/{system_id}/health
```

Each system is isolated by `system_id`.

---

## API Endpoints

### Register or List Systems

```http
POST /systems
GET  /systems
```

Creates or lists known systems. Each system is assigned a unique `system_id`.

---

### Ingest Telemetry Events

```http
POST /systems/{system_id}/events
```

Accepts a batch of telemetry events for a specific system.

#### Request body

```json
{
  "events": [
    {
      "system_id": 3,
      "ts": "2025-12-14T14:33:10.529Z",
      "run_id": "uuid",
      "stage": "extract",
      "event_type": "success",
      "status": "ok",
      "latency_ms": 12,
      "payload": {"rows": 168}
    }
  ]
}
```

#### Validation rules

* `event_type` is required
* `status` must be `ok` or `error`
* `latency_ms` is required
* Invalid payloads return **HTTP 422**

On success, returns **HTTP 202 Accepted**.

---

### System Health

```http
GET /systems/{system_id}/health
```

Returns an aggregated health snapshot for the given system over a recent rolling window.

Example response:

```json
{
  "system_id": 3,
  "window_seconds": 300,
  "window_start": "2025-12-14T14:29:10Z",
  "window_end": "2025-12-14T14:34:10Z",
  "health": "OK",
  "reason": "within thresholds",
  "total": 8,
  "errors": 0,
  "error_rate": 0.0,
  "rps": 0.026,
  "p95_latency": 0.0
}
```

---

## Health Computation Logic

Health is derived from recent telemetry events:

* Events are filtered by `system_id`
* Only events within the rolling time window are considered
* Metrics computed:

  * total events
  * error count
  * error rate
  * request rate (RPS)
  * latency percentiles

Health status rules (example):

* `OK` → error rate below threshold
* `DEGRADED` → elevated error rate
* `UNHEALTHY` → sustained failures

Thresholds are intentionally simple and configurable.

---

## Design Principles

* **Observer-only**: backend never controls pipelines
* **Schema-driven**: strict validation via Pydantic
* **System isolation**: all data scoped by `system_id`
* **Stateless API**: health computed from stored events
* **Composable**: multiple ETLs can reuse the same backend

---

## Running the Backend

```bash
uvicorn app.main:app --reload
```

API documentation available at:

```
http://127.0.0.1:8000/docs
```

---

## What This Backend Demonstrates

* FastAPI request validation
* Event-driven observability design
* Health aggregation patterns
* Clear API contracts between systems
* Real-world handling of 404 vs 422 errors

---

## Relationship to ETL Pipeline

This backend is designed to pair with external ETL systems, such as the **Weather ETL Pipeline**:

* ETL produces telemetry
* Backend ingests and evaluates
* Health endpoint provides operational visibility

The two repositories together demonstrate a complete **producer–observer architecture**.

---

## Status

Backend integration complete.

Verified via live ETL telemetry ingestion and health reporting.
