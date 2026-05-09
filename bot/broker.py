from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict

import yfinance as yf


@dataclass
class Order:
    symbol: str
    side: str
    quantity: float
    price: float
    reason: str


class BrokerClient:
    def __init__(self, mode: str = "paper"):
        self.mode = mode

    def fetch_ohlcv(self, symbol: str, period: str = "2y", interval: str = "1d"):
        return yf.download(symbol, period=period, interval=interval, auto_adjust=True, progress=False)

    def last_price(self, symbol: str) -> float:
        data = self.fetch_ohlcv(symbol, period="5d")
        return float(data["Close"].iloc[-1])

    def place_order(self, order: Order) -> Dict:
        # Replace with MT5/IBKR integration in live mode.
        return {
            "status": "filled",
            "symbol": order.symbol,
            "side": order.side,
            "qty": order.quantity,
            "price": order.price,
            "time": datetime.utcnow().isoformat(),
            "reason": order.reason,
        }

    def next_session_open(self) -> datetime:
        now = datetime.utcnow()
        return now + timedelta(days=1)
