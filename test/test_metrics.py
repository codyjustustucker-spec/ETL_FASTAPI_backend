import pytest
from lso.core.metrics import compute_metrics, p95


def test_no_events():
    m = compute_metrics(total=0, errors=0, latencies_ms=[], window_seconds=60)
    assert m["total"] == 0
    assert m["errors"] == 0
    assert m["error_rate"] == 0.0
    assert m["p95_latency"] is None


def test_all_errors():
    m = compute_metrics(total=5, errors=5, latencies_ms=[
                        10, 20, 30, 40, 50], window_seconds=10)
    assert m["error_rate"] == 1.0


def test_mixed_latencies_p95():
    vals = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    assert p95(vals) == 100.0
