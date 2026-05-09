from dataclasses import dataclass


@dataclass
class Order:
    symbol: str
    side: str
    size: float
    entry: float
    sl: float
    tp: float


class Broker:
    def __init__(self, mode: str = "paper"):
        self.mode = mode

    def place_order(self, order: Order) -> dict:
        return {"status": "filled", **order.__dict__}
