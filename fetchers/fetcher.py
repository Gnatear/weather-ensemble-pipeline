#this file is the base fetcher for all sources
#ABC -> Abstract Base Class
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseFetcher(ABC):
    def fetch_7day_forecast(self, city: str, days: int = 7) -> Dict[str, Any]:
        pass