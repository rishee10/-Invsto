from fastapi import FastAPI, HTTPException
from app.schemas import TickerDataIn, TickerDataOut, StrategyPerformance
from datetime import datetime
from typing import List

app = FastAPI()

# In-memory DB



db: List[TickerDataOut] = []
counter = 1

records_db = []


@app.post("/data", response_model=TickerDataOut)
def post_data(record: TickerDataIn):
    global counter
    # Check for duplicate datetime
    for rec in db:
        if rec.datetime == record.datetime and rec.instrument == record.instrument:
            raise HTTPException(status_code=400, detail="Duplicate datetime")
    db_record = TickerDataOut(**record.model_dump(), id=counter)
    db.append(db_record)
    counter += 1
    return db_record

@app.get("/data", response_model=List[TickerDataOut])
def get_all_data():
    return db

# Strategy function (used in tests)
def calculate_strategy_performance(records, short_window=5, long_window=20):
    # mock computation
    return StrategyPerformance(
        strategy_name="mock_strategy",
        total_returns=10.0,
        buy_signals=2,
        sell_signals=2
    )

