from dataclasses import dataclass
from typing import Optional

class WeatherPoint:
    source: str #api
    timestamp: str #or date
    temperature_c: float #celsius
    wind_speed_ms: Optional[float] = None
    humidity: Optional[float] = None
    predipitation_mm: Optional[float] = None
    condition_code: Optional[str] = None #weather status