from datetime import datetime, timezone
import sqlite3
import json

from lso.db.connection import get_conn


def create_system(name: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()

    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO systems (name, created_at) VALUES (?, ?)",
            (name, now),
        )
        conn.commit()
        system_id = cur.lastrowid

        row = conn.execute(
            "SELECT id, name, created_at FROM systems WHERE id = ?",
            (system_id,),
        ).fetchone()

        return dict(row)
    finally:
        conn.close()


def list_systems() -> list[dict]:
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT id, name, created_at FROM systems ORDER BY id ASC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def system_exists(system_id: int) -> bool:
    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT 1 FROM systems WHERE id = ?", (system_id,)).fetchone()
        return row is not None
    finally:
        conn.close()


def insert_events(system_id: int, events: list[dict]) -> int:
    conn = get_conn()
    try:
        rows = []
        for e in events:
            # e["ts"] is datetime from Pydantic model; store as ISO string
            ts_iso = e["ts"].astimezone(timezone.utc).isoformat()
            rows.append((
                system_id,
                ts_iso,
                e["event_type"],
                e["status"].value if hasattr(
                    e["status"], "value") else str(e["status"]),
                int(e["latency_ms"]),
                json.dumps(e.get("payload", {}), separators=(
                    ",", ":"), ensure_ascii=False),
            ))

        conn.executemany(
            """
            INSERT INTO events (system_id, ts, event_type, status, latency_ms, payload_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
        return len(rows)
    finally:
        conn.close()


def fetch_events_in_window(system_id: int, start_iso: str, end_iso: str) -> list[dict]:
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT ts, status, latency_ms
            FROM events
            WHERE system_id = ?
              AND ts >= ?
              AND ts <= ?
            ORDER BY ts ASC
            """,
            (system_id, start_iso, end_iso),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
