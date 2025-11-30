from pydantic import BaseModel
from typing import List, Optional

class MarketOutcome(BaseModel):
    name: str
    price: float

class MarketEvent(BaseModel):
    id: str
    slug: str
    title: str

class Market(BaseModel):
    id: str
    question: str
    slug: str = ""
    event_slug: str = ""  # New field for parent event slug
    volume_24h: float
    liquidity: float = 0.0
    last_trade_price: Optional[float] = None
    spread: Optional[float] = None
    outcomes: List[MarketOutcome]
    end_date: Optional[str] = None

    class Config:
        from_attributes = True
