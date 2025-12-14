import requests
import uuid
import time
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:8000"
SYSTEM_ID = 3


def iso_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def send_events(total, errors):
    run_id = str(uuid.uuid4())
    events = []

    for i in range(total):
        status = "error" if i < errors else "ok"
        events.append({
            "system_id": SYSTEM_ID,
            "ts": iso_now(),
            "run_id": run_id,
            "stage": "demo",
            "event_type": "demo",
            "status": status,
            "latency_ms": 10,
            "payload": {"i": i},
        })
        time.sleep(0.01)

    r = requests.post(
        f"{BASE_URL}/systems/{SYSTEM_ID}/events",
        json={"events": events},
        timeout=10,
    )

    print("POST:", r.status_code, r.text)


if __name__ == "__main__":
    # CHANGE THESE VALUES PER TEST
    send_events(total=30, errors=0)
