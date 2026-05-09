from .broker import Broker, Order


class TradeExecutor:
    def __init__(self, broker: Broker):
        self.broker = broker

    def execute(self, symbol: str, setup, size: float):
        order = Order(symbol, setup.direction, size, setup.entry, setup.stop, setup.tp)
        return self.broker.place_order(order)
