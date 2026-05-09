from datetime import datetime

from .ai_model import AIModel
from .broker import BrokerClient, Order
from .config import BotConfig
from .dashboard import render_snapshot
from .logger import TradeLogger
from .portfolio_manager import PortfolioManager
from .risk_manager import RiskManager
from .strategy import DipBuyingStrategy


class TradingBot:
    def __init__(self, cfg: BotConfig):
        self.cfg = cfg
        self.broker = BrokerClient(cfg.broker.provider)
        self.strategy = DipBuyingStrategy(cfg.strategy)
        self.risk = RiskManager(cfg.risk)
        self.portfolio = PortfolioManager(cfg.strategy.benchmark_allocations)
        self.logger = TradeLogger(cfg.storage.db_path)
        self.ai = AIModel()

    def run_cycle(self) -> None:
        prices = {}
        for symbol in self.cfg.strategy.symbols:
            data = self.broker.fetch_ohlcv(symbol)
            if data.empty:
                continue
            last_price = float(data["Close"].iloc[-1])
            prices[symbol] = last_price
            current_scale = self.portfolio.positions.get(symbol).scale_level + 1 if symbol in self.portfolio.positions else 0
            signal = self.strategy.evaluate(symbol, data, current_scale=current_scale)
            if signal.action != "BUY":
                continue

            equity = self.portfolio.total_value(prices)
            self.risk.update_equity(equity)
            total_exposure = self.portfolio.exposure(prices)
            scale_weight = self.cfg.strategy.scale_in_levels[signal.scale_level]
            target_notional = equity * self.cfg.strategy.benchmark_allocations[symbol] * scale_weight
            qty = target_notional / last_price

            if not self.risk.can_add_exposure(total_exposure, target_notional / equity):
                continue

            result = self.broker.place_order(Order(symbol, "BUY", qty, last_price, signal.reason))
            self.portfolio.update_position(symbol, qty, last_price, signal.scale_level)
            self.logger.log_trade(
                {
                    "entry_date": result["time"],
                    "exit_date": None,
                    "symbol": symbol,
                    "position_size": qty,
                    "pnl": 0.0,
                    "entry_reason": signal.reason,
                    "exit_reason": None,
                    "ai_confidence": signal.confidence,
                }
            )

        # Exit logic
        for symbol, position in list(self.portfolio.positions.items()):
            data = self.broker.fetch_ohlcv(symbol)
            exit_flags = self.strategy.should_exit(data)
            now_month = datetime.utcnow().month
            should_hold_q4 = now_month in self.cfg.strategy.hold_months
            if exit_flags["trend_reversal"] or (not should_hold_q4 and exit_flags["momentum_breakdown"]):
                px = float(data["Close"].iloc[-1])
                pnl = (px - position.avg_price) * position.quantity
                self.portfolio.close_position(symbol, px)
                self.logger.log_trade(
                    {
                        "entry_date": position.opened_at.isoformat(),
                        "exit_date": datetime.utcnow().isoformat(),
                        "symbol": symbol,
                        "position_size": position.quantity,
                        "pnl": pnl,
                        "entry_reason": "scaled dip entries",
                        "exit_reason": "trend reversal / momentum breakdown",
                        "ai_confidence": 0.5,
                    }
                )

        eq = self.portfolio.total_value(prices if prices else {})
        self.risk.update_equity(eq)
        ai = self.ai.classify_regime(volatility=0.35, trend_strength=0.7)
        snapshot = render_snapshot(
            {
                "portfolio_value": eq,
                "exposure": self.portfolio.exposure(prices if prices else {}),
                "drawdown": 0 if self.risk.state.high_watermark == 0 else 1 - eq / self.risk.state.high_watermark,
                "ai_confidence": ai.confidence,
                "trend_status": ai.regime,
                "open_trades": len(self.portfolio.positions),
                "risk_alerts": "CIRCUIT BREAKER" if self.risk.state.circuit_breaker_engaged else "OK",
            }
        )
        print(snapshot)


if __name__ == "__main__":
    bot = TradingBot(BotConfig())
    bot.run_cycle()
