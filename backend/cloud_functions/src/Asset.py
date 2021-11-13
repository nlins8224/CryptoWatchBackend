from dataclasses import dataclass
import json


@dataclass
class Asset:
    id: str
    symbol: str
    name: str
    price: float
    market_cap: float
    market_cap_rank: int
    total_volume: float
    high: float
    low: float
    price_change: float
    price_change_percentage: float
    market_cap_change: float
    last_updated: str

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
