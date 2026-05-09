from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class BotConfig:
    mode: str = "paper"  # backtest|paper|live
    symbols: List[str] = field(default_factory=lambda: ["US30", "NAS100", "SPX500", "XAUUSD", "EURUSD"])
    htf_timeframes: List[str] = field(default_factory=lambda: ["1d", "4h"])
    structure_timeframes: List[str] = field(default_factory=lambda: ["1h", "15m"])
    entry_timeframes: List[str] = field(default_factory=lambda: ["5m", "1m"])
    risk_per_trade: float = 0.01
    max_daily_loss_r: float = 3.0
    max_weekly_loss_r: float = 6.0
    breakeven_at_1r: bool = True
    trailing_after_1r: bool = True
    min_displacement_atr: float = 1.2
    ote_zone: tuple = (0.62, 0.70)
    optional_ote: float = 0.79
    correlation_map: Dict[str, Dict[str, str]] = field(
        default_factory=lambda: {
            "US30": {"DXY": "inverse", "VIX": "inverse"},
            "NAS100": {"DXY": "inverse", "VIX": "inverse"},
            "SPX500": {"DXY": "inverse", "VIX": "inverse"},
        }
    )
