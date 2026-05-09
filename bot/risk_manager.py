from dataclasses import dataclass

from .config import RiskConfig


@dataclass
class RiskState:
    high_watermark: float
    circuit_breaker_engaged: bool = False


class RiskManager:
    def __init__(self, cfg: RiskConfig):
        self.cfg = cfg
        self.state = RiskState(high_watermark=0.0)

    def update_equity(self, equity: float) -> None:
        self.state.high_watermark = max(self.state.high_watermark, equity)
        if self.state.high_watermark <= 0:
            return
        drawdown = 1 - (equity / self.state.high_watermark)
        self.state.circuit_breaker_engaged = drawdown >= self.cfg.circuit_breaker_drawdown

    def position_size(self, equity: float, entry: float, stop: float) -> float:
        risk_capital = equity * self.cfg.risk_per_trade
        per_unit_risk = max(entry - stop, 1e-8)
        return max(risk_capital / per_unit_risk, 0.0)

    def can_add_exposure(self, current_exposure: float, additional: float) -> bool:
        return (current_exposure + additional) <= self.cfg.max_portfolio_exposure and not self.state.circuit_breaker_engaged
