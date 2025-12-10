import pytest
import requests
from typing import Any, Dict
from fetchers.open_meteo import OpenMeteoFetcher

class DummyResponse:
    def __init__(self, json_data: Dict[str, Any], status_code: int = 200) -> None:
        self._json_data = json_data
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if not (200 <= self.status_code < 300):
            raise Exception(f"HTTP err {self.status_code}")
        
    def json(self) -> Dict[str, Any]:
        return self._json_data
    
def test_open_meteo_fetcher_calls_requests_with_correct_params(monkeypatch: pytest.MonkeyPatch):
    captured_params = {}

    def fake_get(url: str, params: Dict[str, Any], timeout: int = 10, **kwargs: Any):
        captured_params["url"] = url
        captured_params["params"] = params
        dummy_json = {"ok": True, "hourly": {"time": [], "temperature_2m": []}}
        return DummyResponse(dummy_json)
    
    monkeypatch.setattr(requests, "get", fake_get)

    f = OpenMeteoFetcher(lat = 44.6488, lon = -63.5752)
    
    resslt = f.fetch_7day_forecast(city = "Halifax", days = 7)

    assert resslt["ok"] is True

    assert "open-meteo.com" in captured_params["url"]

    params = captured_params["params"]
    assert float(params["latitude"]) == 44.6488
    assert float(params["longitude"]) == -63.5752
    assert int(params["forecast_days"]) == 7
    assert "temperature_2m" in params["hourly"]