from typing import Any, Dict
import requests
from fetchers.fetcher import BaseFetcher

class OpenMeteoFetcher(BaseFetcher):

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    # returns json
    def fetch_7day_forecast(self, city: str, days: int = 7) -> Dict[str, Any]:

        hourly_vars = [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
        ]
        # open meteo based on coordination
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "hourly": ",".join(hourly_vars),
            "forecast_days": days,
            "timezone": "auto",
        }

        response = requests.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status() # throw err if not 200

        return response.json()
