from __future__ import annotations
import argparse
import time
import uuid
from datetime import datetime, timezone
import requests


def iso_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://127.0.0.1:8000")
    ap.add_argument("--system-id", type=int, required=True)
    ap.add_argument("--count", type=int, default=20)
    ap.add_argument("--errors", type=int, default=0)   # number of error events
    ap.add_argument("--latency-ms", type=int, default=0)
    ap.add_argument("--stage", default="extract")
    ap.add_argument("--event-type", default="demo")
    args = ap.parse_args()

    url = args.base_url.rstrip("/") + f"/systems/{args.system_id}/events"
    run_id = str(uuid.uuid4())

    events = []
    for i in range(args.count):
        status = "error" if i < args.errors else "ok"
        events.append({
            "system_id": args.system_id,
            "ts": iso_now(),
            "run_id": run_id,
            "stage": args.stage,
            "event_type": args.event_type,
            "status": status,              # must be ok|error
            "latency_ms": args.latency_ms,  # required
            "payload": {"i": i},
        })
        time.sleep(0.02)  # tiny spread so timestamps differ

    r = requests.post(url, json={"events": events}, timeout=10)
    print(r.status_code, r.text[:300])


if __name__ == "__main__":
    main()
