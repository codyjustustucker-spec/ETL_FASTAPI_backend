from datetime import datetime, timezone

import pytest

from lso.core.windowing import window_bounds


def test_window_bounds_utc_naive_end_forced_to_utc():
    end = datetime(2025, 1, 1, 0, 0, 10)  # naive
    start, end2 = window_bounds(10, end=end)
    assert end2.tzinfo == timezone.utc
    assert start.tzinfo == timezone.utc
    assert (end2 - start).total_seconds() == 10


def test_window_bounds_aware_end_converted_to_utc():
    end = datetime(2025, 1, 1, 0, 0, 10, tzinfo=timezone.utc)
    start, end2 = window_bounds(60, end=end)
    assert end2.tzinfo == timezone.utc
    assert (end2 - start).total_seconds() == 60


def test_window_bounds_rejects_nonpositive():
    with pytest.raises(ValueError):
        window_bounds(0)
