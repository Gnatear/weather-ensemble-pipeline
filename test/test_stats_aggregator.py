from models.normalizer import WeatherPoint
from stats.aggregator import (
    aggregate_by_timestamp, compute_mean_sd, detect_outliers,
)

def _make_point(ts: str, temp: float, source: str = "test") -> WeatherPoint:
    return WeatherPoint(
        source = source,
        timestamp = ts,
        temperature_c = temp,
    )

def test_aggregate_by_timestamp_groups_correctly():

    points = [
        _make_point("2025-01-01T10:00", 1.0, source = "a"),
        _make_point("2025-01-01T10:00", 2.0, source = "a"),
        _make_point("2025-01-01T11:00", 3.0, source = "a"),
    ]

    grouped = aggregate_by_timestamp(points)
    assert set(grouped.keys()) == {"2025-01-01T10:00", "2025-01-01T11:00"}
    assert len(grouped["2025-01-01T10:00"]) == 2
    assert len(grouped["2025-01-01T11:00"]) == 1

def test_compute_mean_sd_basic():
    values = [1.0, 2.0, 3.0]
    mean, sd = compute_mean_sd(values)

    assert 0.8 < sd < 1.0

def test_detect_outliers_simple_case():
    values = [10.0, 99.9, 11.0, 9.0]
    flags = detect_outliers(values, z_threshold = 2.0)

    assert len(flags) == len(values)
    assert flags[0] is False
    assert flags[1] is True
    assert flags[2] is False
    assert flags[3] is False