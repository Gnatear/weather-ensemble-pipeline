from typing import Dict, Any, List
from config.initializer import (
    DEFAULT_CITY,
    DEFAULT_DAYS,
    DEFAULT_LAT,
    DEFAULT_LON,
)
from fetchers.open_meteo import OpenMeteoFetcher
from models.normalizer import WeatherPoint, normalize_open_meteo
from stats.aggregator import (
    aggregate_by_timestamp,
    compute_mean_sd,
    detect_outliers,
)

def run(city: str | None = None, days: int | None = None) -> Dict [str, Any]:
    
    city = city or DEFAULT_CITY
    days = days or DEFAULT_DAYS

    open_meteo_fetcher = OpenMeteoFetcher(lat = DEFAULT_LAT, lon = DEFAULT_LON)

    raw_open_meteo = open_meteo_fetcher.fetch_7day_forecast(city = city, days = days)

    points: List[WeatherPoint] = []
    points.extend(normalize_open_meteo(raw_open_meteo, source_name = "open_meteo"))
    # addition fetcher will be added here
    grouped = aggregate_by_timestamp(points)

    timestamps_stats = []
    for ts, pts in sorted(grouped.items(), key = lambda x: x[0]):
        temps = [p.temperature_c for p in pts if p.temperature_c is not None]

        mean_temp, sd_temp = compute_mean_sd(temps)
        outlier_flags = detect_outliers(temps, z_threshold = 2.5)

        outlier_sources = [pts[i].source for i, is_outlier in neumerate(outlier_flags) if is_outlier]

        timestamps_stats.append(
            {
                "timestamp": ts,
                "n_points": len(temps),
                "temperature_c": {
                    "values": temps,
                    "mean": mean_temp,
                    "sd": sd_temp,
                    "outlier_sources": outlier_sources,
                }
            }
        )
    result: Dict[str, Any] = {
        "city": city,
        "days": days,
        "source_count": 1,
        "timestamps": timestamps_stats,
    }

    return result