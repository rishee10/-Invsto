from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TickerDataIn(BaseModel):
    datetime: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    instrument: str

class TickerDataOut(TickerDataIn):
    id: int  # required by tests

class StrategyPerformance(BaseModel):
    strategy_name: str
    total_returns: float
    buy_signals: int
    sell_signals: int
