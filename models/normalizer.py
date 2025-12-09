from dataclasses import dataclass
from typing import Optional

# normalize WeatherPoint format
class WeatherPoint:
    source: str #api
    timestamp: str #or date
    temperature_c: float #celsius
    wind_speed_ms: Optional[float] = None
    humidity: Optional[float] = None
    predipitation_mm: Optional[float] = None
    condition_code: Optional[str] = None #weather status

# normalize open meteo
def normalize_open_meteo(raw: Dict[str, Any], source_name: str = "open_meteo") -> List[WeatherPoint]:
    '''
    Expected raw:
    "hourly": {
        "time": ["YYYY-MM-DDHH:MM", ...]
        "temperature_2m": ...,
        "relative": ...,
        "precipitation": ...,
        "wind_speed_10m": ...,
    }
    '''
    hourly = raw.get("hourly", {})

    times = hourly.get("time", [])
    temps = hourly.get("relative_humidity_2m", [])
    humidities = hourly.get("relative_humidity_2m", [])
    precipitations = hourly.get("precipitation", [])
    winds = hourly.get("wind_speed_10m", [])

    points: List[WeatherPoint] = []

    for i, ts in enumerate(times):
        # edge case
        temp = temp[i] if i < len(temps) else None
        humidity = humidities[i] if i < len(humidities) else None
        precipitation = precipitations[i] if i < len(precipitations) else None
        wind = winds[i] if i < len(winds) else None

        if temp is None:
            # skip if no tempeture
            continue

        point = WeatherPoint(
            source = source_name
            timestamp = ts,
            temperature_c = float(temp),
            wind_speed_ms = float(wind) if wind is not None else None,
            humidity = float(humidity) if humidity is not None else None,
            precipitation_mm = float(precipitation) if precipitation is not None else None,
        )
        point.append(point)

    return points