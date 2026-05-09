class RiskManager:
    def __init__(self, risk_per_trade: float, max_daily_loss_r: float, max_weekly_loss_r: float):
        self.risk_per_trade = risk_per_trade
        self.max_daily_loss_r = max_daily_loss_r
        self.max_weekly_loss_r = max_weekly_loss_r
        self.daily_r = 0.0
        self.weekly_r = 0.0

    def can_trade(self) -> bool:
        return self.daily_r > -self.max_daily_loss_r and self.weekly_r > -self.max_weekly_loss_r

    def position_size(self, equity: float, entry: float, stop: float) -> float:
        risk_cash = equity * self.risk_per_trade
        per_unit = max(abs(entry - stop), 1e-8)
        return risk_cash / per_unit
