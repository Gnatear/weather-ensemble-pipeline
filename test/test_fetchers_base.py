import pytest
from typing import Any, Dict
from fetchers.fetcher import BaseFetcher

def test_base_fetcher_cannot_instantiate():
    with pytest.raises(TypeError):
        BaseFetcher

def test_child_without_implementation_cannot_instantiate():
    #fetch_7day_forecast
    class BadFetcher(BaseFetcher):
        pass

    with pytest.raises(TypeError):
        BadFetcher()

def test_child_with_implementation_can_instantiate():
    class GoodFetcher(BaseFetcher):
        def fetch_7day_forecast(self, city: str, days: int = 7) -> Dict[str, Any]:
            return {"city": city, "days": days, "ok": Any}
        
    f = GoodFetcher()
    result = f.fetch_7day_forecast("halifax", days = 3)

    assert result["city"] == "Halifax"
    assert result["days"] == 3
    assert result["ok"] is True
        