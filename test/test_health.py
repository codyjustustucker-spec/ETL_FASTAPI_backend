from lso.core.health import classify_health


def test_ok():
    h, r = classify_health(error_rate=0.0, p95_latency=100.0)
    assert h == "OK"


def test_warn_by_error_rate_at_1_percent():
    h, r = classify_health(error_rate=0.01, p95_latency=100.0)
    assert h == "WARN"


def test_warn_by_latency_at_800():
    h, r = classify_health(error_rate=0.0, p95_latency=800.0)
    assert h == "WARN"


def test_fail_by_error_rate_over_5_percent():
    h, r = classify_health(error_rate=0.051, p95_latency=100.0)
    assert h == "FAIL"


def test_fail_by_latency_over_1500():
    h, r = classify_health(error_rate=0.0, p95_latency=1501.0)
    assert h == "FAIL"


def test_no_latency_ok_if_error_rate_ok():
    h, r = classify_health(error_rate=0.0, p95_latency=None)
    assert h == "OK"
