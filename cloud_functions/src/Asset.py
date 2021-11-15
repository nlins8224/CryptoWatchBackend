from dataclasses import dataclass
import json


@dataclass
class Asset:
    id: str = None
    symbol: str = None
    name: str = None
    price: float = None
    market_cap: float = None
    market_cap_rank: int = None
    total_volume: float = None
    high: float = None
    low: float = None
    price_change: float = None
    price_change_percentage: float = None
    market_cap_change: float = None
    last_updated: str = None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
