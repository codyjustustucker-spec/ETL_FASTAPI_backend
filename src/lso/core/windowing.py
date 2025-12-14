from datetime import datetime, timedelta, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def window_bounds(window_seconds: int, end: datetime | None = None) -> tuple[datetime, datetime]:
    if window_seconds <= 0:
        raise ValueError("window_seconds must be > 0")

    end_dt = end or utc_now()

    # force UTC
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    else:
        end_dt = end_dt.astimezone(timezone.utc)

    start_dt = end_dt - timedelta(seconds=window_seconds)
    return start_dt, end_dt
