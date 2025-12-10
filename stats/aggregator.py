#this file will aggregate data from different sources and divide them by ts
#and get mean, ds, outliner

from typing import List, Dict, Tuple
import numpy as np
from models.normalizer import WeatherPoint

def aggregate_by_timestamp(points: List[WeatherPoint]) -> Dict[str, List[WeatherPoint]]:
    groups: Dict[str, List[WeatherPoint]] = {}
    # key is timestamp
    for p in points:
        groups.setdefault(p.timestamp, []).append(p)
    return groups

def compute_mean_sd(values: List[float]) -> Tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    
    arr = np.array(values, dtype = float)
    mean = float(arr.mean())
    #sd for sample
    sd = float(arr.std(ddof = 1))

    return mean, sd

def detect_outliers(values: List[float], z_threshold: float = 2.5) -> List[bool]:
    #z_score -> if |z| > z_threshold -> outlier

    if not values:
        return []
    
    arr = np.array(values, dtype = float)
    mean = arr.mean()
    sd = arr.std(ddof = 0)

    if sd == 0:
        return [False] * len(values)
    
    z_scores = (arr - mean) / sd

    return [abs(z) > z_threshold for z in z_scores]