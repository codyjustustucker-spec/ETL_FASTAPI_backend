from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging

from fastapi import FastAPI

from lso.logging_config import setup_logging
from lso.settings import settings
from lso.db.migrate import run_migrations

from lso.api.routes_systems import router as systems_router
from lso.api.routes_events import router as events_router
from lso.api.routes_metrics import router as metrics_router


setup_logging()

log = logging.getLogger("lso")
log.info(f"boot env={settings.LSO_ENV} db={settings.LSO_DB_URL}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()
    yield


app = FastAPI(
    title="Living Systems Observatory",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(systems_router)
app.include_router(events_router)
app.include_router(metrics_router)


@app.get("/healthz")
def healthz():
    return {
        "ok": True,
        "time": datetime.now(timezone.utc).isoformat(),
    }
