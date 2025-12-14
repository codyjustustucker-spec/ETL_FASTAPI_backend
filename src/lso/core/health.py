from lso.settings import settings


def classify_health(error_rate: float, p95_latency: float | None) -> tuple[str, str]:
    # FAIL if either metric is beyond FAIL threshold
    if error_rate > settings.LSO_WARN_ERROR_RATE:
        return "FAIL", f"error_rate > {settings.LSO_WARN_ERROR_RATE:.2%}"

    if p95_latency is not None and p95_latency > settings.LSO_WARN_P95_MS:
        return "FAIL", f"p95_latency_ms > {settings.LSO_WARN_P95_MS}"

    # WARN if either metric is beyond OK threshold
    if error_rate >= settings.LSO_OK_ERROR_RATE:
        return "WARN", f"error_rate >= {settings.LSO_OK_ERROR_RATE:.2%}"

    if p95_latency is not None and p95_latency >= settings.LSO_OK_P95_MS:
        return "WARN", f"p95_latency_ms >= {settings.LSO_OK_P95_MS}"

    return "OK", "within thresholds"
