import pytest
from typing import Any, Dict
from pipeline.run_pipeline import run as run_pipeline
from fetchers.open_meteo import OpenMeteoFetcher

def _fake_raw_open_meteo() -> Dict[str, Any]:
    return{
        "hourly":{
            "time": ["2025-01-01T10:00", "2025-01-01T11:00"],
            "temperature_2m": [1.0, 3.0],
            "relative_humidity_2m": [80, 82],
            "precipitation": [0.0, 0.2],
            "wind_speed_10m": [3.0, 4.0]
        }
    }

def test_pipeline_run_with_mocked_open_meteo(monkeypatch: pytest.MonkeyPatch):
    def fake_fetch(self, city: str, days: int = 7) -> Dict[str, Any]:
        return _fake_raw_open_meteo()
    
    monkeypatch.setattr(OpenMeteoFetcher, "fetch_7day_forecast", fake_fetch)

    result = run_pipeline(city = "Halifax", days = 2)

    assert result["city"] == "Halifax"
    assert result["days"] == 2
    assert result["source_count"] == 1

    timestamps = result["timestamps"]
    assert len(timestamps) == 2

    first = timestamps[0]
    assert first["timestamp"] == "2025-01-01T10:00"
    temp_info = first["temperature_c"]
    assert temp_info["mean"] == 1.0
    assert temp_info["sd"] == 0.0