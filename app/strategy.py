# app/strategy.py
from typing import List, Dict
from datetime import datetime
from decimal import Decimal
import numpy as np

def moving_average(series: List[float], window: int) -> List[float]:
    if window <= 0:
        raise ValueError("window must be > 0")
    arr = np.array(series, dtype=float)
    if len(arr) < window:
        return [None] * len(arr)
    ma = np.convolve(arr, np.ones(window)/window, mode='valid')
    # left-pad with None to maintain same length
    pad = [None] * (window - 1)
    return pad + ma.tolist()

def compute_signals(dates: List[datetime], closes: List[float], short_w: int = 20, long_w: int = 50) -> Dict:
    if long_w <= short_w:
        raise ValueError("long_w must be greater than short_w")
    short_ma = moving_average(closes, short_w)
    long_ma = moving_average(closes, long_w)

    position = 0  # 1 if long, 0 if flat
    trades = []
    for i in range(len(closes)):
        s = short_ma[i]
        l = long_ma[i]
        if s is None or l is None:
            continue
        # crossover up => buy
        if s > l and position == 0:
            trades.append({"date": dates[i].isoformat(), "action": "BUY", "price": closes[i], "index": i})
            position = 1
        # crossover down => sell
        elif s < l and position == 1:
            trades.append({"date": dates[i].isoformat(), "action": "SELL", "price": closes[i], "index": i})
            position = 0

    # If still long at end, close at last price
    if position == 1:
        trades.append({"date": dates[-1].isoformat(), "action": "SELL", "price": closes[-1], "index": len(closes)-1})

    # Evaluate performance: simple return assuming full capital invested on buys and all sold on sells, no slippage
    pnl = 0.0
    for i in range(0, len(trades), 2):
        if i+1 >= len(trades):
            break
        buy = trades[i]
        sell = trades[i+1]
        pnl += (sell["price"] - buy["price"]) / buy["price"]

    # Convert to percentage
    total_return = pnl * 100
    return {
        "trades": trades,
        "total_return_percent": total_return,
        "num_trades": len(trades)//2
    }
