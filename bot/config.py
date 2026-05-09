from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class BrokerConfig:
    provider: str = "paper"  # paper | mt5 | ibkr
    live_trading: bool = False
    dry_run: bool = True


@dataclass
class RiskConfig:
    risk_per_trade: float = 0.01
    max_portfolio_exposure: float = 0.80
    max_symbol_exposure: float = 0.40
    max_drawdown: float = 0.15
    trailing_stop_atr_mult: float = 2.5
    circuit_breaker_drawdown: float = 0.20


@dataclass
class StrategyConfig:
    symbols: List[str] = field(default_factory=lambda: ["^DJI", "^GSPC", "^NDX"])
    benchmark_allocations: Dict[str, float] = field(
        default_factory=lambda: {"^NDX": 0.40, "^GSPC": 0.30, "^DJI": 0.30}
    )
    ema_fast: int = 50
    ema_slow: int = 200
    ema_pullback_1: int = 20
    rsi_buy_threshold: float = 45.0
    rsi_deep_buy_threshold: float = 40.0
    atr_window: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    scale_in_levels: List[float] = field(default_factory=lambda: [0.25, 0.25, 0.25, 0.25])
    hold_months: List[int] = field(default_factory=lambda: [11, 12])
    skip_event_days: bool = True
    rebalance_days: int = 20


@dataclass
class StorageConfig:
    db_path: Path = Path("trading_bot.db")


@dataclass
class BotConfig:
    broker: BrokerConfig = field(default_factory=BrokerConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    strategy: StrategyConfig = field(default_factory=StrategyConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
