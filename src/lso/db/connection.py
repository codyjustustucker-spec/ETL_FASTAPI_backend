import sqlite3
from pathlib import Path
from lso.settings import settings


def get_conn() -> sqlite3.Connection:
    # expects sqlite:///data/lso.db
    db_url = settings.LSO_DB_URL
    if not db_url.startswith("sqlite:///"):
        raise ValueError("Only sqlite:/// paths supported in MVP")

    rel_path = db_url.removeprefix("sqlite:///")
    Path(rel_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(rel_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
