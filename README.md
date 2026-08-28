# LSO — Telemetry & Health Service

**A working FastAPI observability backend that receives structured telemetry from external systems and turns it into rolling system-health metrics.**

**Python • FastAPI • Pydantic • REST APIs • Event Processing • Observability**

- ✅ Accepts telemetry from external systems
- ✅ Validates structured event payloads
- ✅ Stores telemetry events
- ✅ Computes rolling health metrics
- ✅ Isolates data by system
- ✅ Integrated and verified with the Weather ETL Pipeline

---

## What It Does

LSO (**Living Systems Observatory**) is a lightweight backend designed to observe other software systems.

External systems send structured telemetry events to LSO. The service validates and stores those events, then calculates health information over a rolling time window.

```text
External Systems
       │
       │ telemetry events
       ▼
┌─────────────────────┐
│       LSO API       │
│      FastAPI        │
└─────────┬───────────┘
          │
          ▼
   Schema Validation
          │
          ▼
      Event Store
          │
          ▼
   Health Aggregator
          │
          ▼
 OK / DEGRADED / UNHEALTHY
```

LSO is deliberately an **observer, not an orchestrator**.

It does not run ETL jobs or control external pipelines. Producers remain independent and report telemetry into the service.

Multiple systems can report into a single LSO instance.

---

## Core Responsibilities

LSO provides five main capabilities:

1. **Register systems**
2. **Receive telemetry events**
3. **Validate incoming event schemas**
4. **Store and aggregate recent telemetry**
5. **Expose calculated health through a REST API**

Each monitored system is isolated using its own `system_id`.

---

## API

### Register a System

```http
POST /systems
```

Creates a known system and assigns it a unique `system_id`.

### List Systems

```http
GET /systems
```

Returns registered systems.

---

### Submit Telemetry

```http
POST /systems/{system_id}/events
```

Accepts a batch of structured telemetry events for a specific system.

Example:

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
      "payload": {
        "rows": 168
      }
    }
  ]
}
```

### Validation

Incoming events are schema validated.

Examples of enforced requirements include:

- `event_type` is required
- `status` must be `ok` or `error`
- `latency_ms` is required
- malformed payloads return **HTTP 422**

Successfully accepted telemetry returns:

```text
HTTP 202 Accepted
```

---

### Query System Health

```http
GET /systems/{system_id}/health
```

Returns a health snapshot calculated from telemetry within a recent rolling time window.

Example:

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

## Health Computation

Health is calculated from recent telemetry rather than being directly reported by the monitored system.

For a requested `system_id`, LSO:

```text
Stored Events
     │
     ▼
Filter by System
     │
     ▼
Filter by Time Window
     │
     ▼
Aggregate Metrics
     │
     ▼
Evaluate Thresholds
     │
     ▼
Health Result
```

Metrics include:

- total events
- error count
- error rate
- request rate (RPS)
- latency percentiles

Health can resolve to states such as:

```text
OK
DEGRADED
UNHEALTHY
```

Thresholds are intentionally simple and configurable.

---

## Architecture Decisions

### Observer-Only

LSO observes external systems without controlling them.

This keeps monitoring concerns separate from the systems being monitored.

### Schema-Driven

Telemetry contracts are explicitly validated before events are accepted.

This prevents malformed data from silently entering the observability system.

### System Isolation

Telemetry is scoped by `system_id`, allowing multiple independent producers to use the same backend.

### Derived Health

Health is calculated from stored telemetry over a rolling window rather than maintained as arbitrary mutable state.

### Composable

The service is designed so different pipelines, workers, or services can report through the same telemetry contract.

---

## Weather ETL Integration

LSO has been integrated with the **Weather ETL Pipeline** as a real telemetry producer.

```text
Weather ETL Pipeline
        │
        │ produces telemetry
        ▼
   LSO Backend
        │
        ├── validates events
        ├── stores events
        └── aggregates metrics
                │
                ▼
           Health API
```

This creates a simple **producer–observer architecture**:

- the ETL pipeline performs its own work
- the ETL emits operational telemetry
- LSO receives and evaluates that telemetry
- clients can query LSO for health information

[View the Weather ETL Pipeline](https://github.com/codyjustustucker-spec/Weather-ETL-Pipeline)

---

## Running Locally

Start the FastAPI service:

```bash
uvicorn app.main:app --reload
```

Once running, interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

FastAPI's generated documentation can be used to inspect endpoints and submit requests directly.

---

## What This Project Demonstrates

This project demonstrates practical backend and systems-engineering concepts including:

- REST API design
- FastAPI application development
- Pydantic request validation
- explicit API contracts
- event-driven system boundaries
- telemetry ingestion
- rolling-window aggregation
- health metric computation
- multi-system isolation
- error handling
- HTTP `404`, `422`, and `202` behavior
- separation of monitoring from execution
- integration between independent software systems

---

## Project Scope

LSO is intentionally small and focused.

It is not intended to be a full infrastructure-monitoring platform or an ETL orchestrator. Its purpose is to demonstrate a clean telemetry contract and a reusable backend capable of observing multiple independent systems.

Keeping those responsibilities narrow makes the architecture easier to reason about, test, integrate, and extend.

---

## Status

**Backend integration complete.**

Telemetry ingestion and health reporting have been verified through integration with the Weather ETL Pipeline.
