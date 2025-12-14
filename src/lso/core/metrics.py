import math
from typing import Iterable


def p95(values: list[int]) -> float | None:
    if not values:
        return None
    vals = sorted(values)
    # "nearest-rank" style
    k = math.ceil(0.95 * len(vals)) - 1
    k = max(0, min(k, len(vals) - 1))
    return float(vals[k])


def compute_metrics(
    total: int,
    errors: int,
    latencies_ms: list[int],
    window_seconds: int,
) -> dict:
    if window_seconds <= 0:
        raise ValueError("window_seconds must be > 0")

    if total < 0 or errors < 0:
        raise ValueError("total/errors must be >= 0")

    if errors > total:
        raise ValueError("errors cannot exceed total")

    error_rate = (errors / total) if total else 0.0
    rps = total / window_seconds

    return {
        "total": total,
        "errors": errors,
        "error_rate": error_rate,
        "rps": rps,
        "p95_latency": p95(latencies_ms),
    }
