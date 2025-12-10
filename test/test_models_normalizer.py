from models.normalizer import WeatherPoint, normalize_open_meteo

def test_weather_point_detaclass_basic():
    p = WeatherPoint(
        source = "test_api",
        timestamp = "2025-01-01T10:00",
        temperature_c = 1.5,
        wind_speed_ms = 3.2,
        humidity = 80.0,
        precipitation_mm = 0.1,
        condition_code = "rain",
    )

    assert p.source == "test_api"
    assert p.timestamp == "2025-01-01T10:00"
    assert p.temperature_c == 1.5
    assert p.wind_speed_ms == 3.2
    assert p.humidity == 80.0
    assert p.precipitation_mm == 0.1
    assert p.condition_code == "rain"

def test_normalize_open_meteo_basic():
    raw = {
        "hourly":{
            "time": ["2025-12-30T10:00", "2025-12-30T11:00", "2025-12-30T12:00"],
            "temperature_2m": [1.0, 2.5, 3.4],
            "relative_humidity_2m": [80, 82, 85],
            "precipitation": [0.0, 0.1, 0.3],
            "wind_speed_10m": [3.5, 4.0, 6.5],
        }
    }

    points = normalize_open_meteo(raw, source_name = "open_meteo")

    assert len(points) == 3
    assert all(isinstance(p, WeatherPoint) for p in points)

    p0 = points[0]
    assert p0.source == "open_meteo"
    assert p0.timestamp == "2025-12-30T10:00"
    assert p0.temperature_c == 1.0
    assert p0.humidity == 80.0
    assert p0.precipitation_mm == 0.0
    assert p0.wind_speed_ms == 3.5