from lso.db.connection import get_conn

SYSTEMS_SQL = """
CREATE TABLE IF NOT EXISTS systems (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL
);
"""

EVENTS_SQL = """
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  system_id INTEGER NOT NULL,
  ts TEXT NOT NULL,
  event_type TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('ok','error')),
  latency_ms INTEGER NOT NULL CHECK (latency_ms >= 0),
  payload_json TEXT NOT NULL,
  FOREIGN KEY(system_id) REFERENCES systems(id) ON DELETE CASCADE
);
"""

INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_events_system_ts ON events(system_id, ts);
"""


def run_migrations() -> None:
    conn = get_conn()
    try:
        conn.execute(SYSTEMS_SQL)
        conn.execute(EVENTS_SQL)
        conn.execute(INDEXES_SQL)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    run_migrations()
    print("migrations ok")
