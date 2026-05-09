from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class Position:
    symbol: str
    quantity: float
    avg_price: float
    scale_level: int = 0
    opened_at: datetime = field(default_factory=datetime.utcnow)


class PortfolioManager:
    def __init__(self, target_weights: Dict[str, float]):
        self.target_weights = target_weights
        self.positions: Dict[str, Position] = {}
        self.cash = 1_000_000.0

    def total_value(self, prices: Dict[str, float]) -> float:
        positions_value = sum(pos.quantity * prices.get(sym, pos.avg_price) for sym, pos in self.positions.items())
        return self.cash + positions_value

    def exposure(self, prices: Dict[str, float]) -> float:
        tv = self.total_value(prices)
        if tv <= 0:
            return 0.0
        return (tv - self.cash) / tv

    def update_position(self, symbol: str, qty: float, price: float, scale_level: int) -> None:
        cost = qty * price
        self.cash -= cost
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol, qty, price, scale_level)
            return
        pos = self.positions[symbol]
        new_qty = pos.quantity + qty
        pos.avg_price = (pos.quantity * pos.avg_price + cost) / new_qty
        pos.quantity = new_qty
        pos.scale_level = scale_level

    def close_position(self, symbol: str, price: float) -> None:
        pos = self.positions.pop(symbol, None)
        if not pos:
            return
        self.cash += pos.quantity * price
