from dataclasses import dataclass
from typing import Dict, Optional

import pandas as pd

from .config import StrategyConfig
from .indicators import atr, ema, higher_highs_higher_lows, macd, rsi


@dataclass
class Signal:
    symbol: str
    action: str
    confidence: float
    reason: str
    scale_level: int = 0


class DipBuyingStrategy:
    def __init__(self, cfg: StrategyConfig):
        self.cfg = cfg

    def prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        out["ema20"] = ema(out["Close"], self.cfg.ema_pullback_1)
        out["ema50"] = ema(out["Close"], self.cfg.ema_fast)
        out["ema200"] = ema(out["Close"], self.cfg.ema_slow)
        out["rsi"] = rsi(out["Close"])
        out["atr"] = atr(out, self.cfg.atr_window)
        out["macd"], out["macd_signal"], out["macd_hist"] = macd(
            out["Close"], self.cfg.macd_fast, self.cfg.macd_slow, self.cfg.macd_signal
        )
        return out

    def bullish_macro_trend(self, df: pd.DataFrame) -> bool:
        row = df.iloc[-1]
        return (
            row["Close"] > row["ema200"]
            and row["ema50"] > row["ema200"]
            and higher_highs_higher_lows(df)
        )

    def evaluate(self, symbol: str, df: pd.DataFrame, current_scale: int = 0) -> Optional[Signal]:
        df = self.prepare(df)
        last = df.iloc[-1]
        prev = df.iloc[-2]

        if not self.bullish_macro_trend(df):
            return Signal(symbol, "HOLD", 0.2, "Macro trend not bullish")

        near_ema_pullback = (last["Close"] <= last["ema20"]) or (last["Close"] <= last["ema50"])
        rsi_dip = last["rsi"] < self.cfg.rsi_buy_threshold
        deep_dip = last["rsi"] < self.cfg.rsi_deep_buy_threshold
        momentum_recovery = last["macd_hist"] > prev["macd_hist"]
        atr_contracting = last["atr"] <= df["atr"].tail(10).mean()

        if near_ema_pullback and rsi_dip and momentum_recovery and atr_contracting:
            level = min(current_scale, len(self.cfg.scale_in_levels) - 1)
            confidence = 0.6 + (0.2 if deep_dip else 0.0) + (0.1 if last["Close"] <= last["ema50"] else 0.0)
            return Signal(symbol, "BUY", min(confidence, 0.95), "Healthy dip in bullish trend", level)

        return Signal(symbol, "HOLD", 0.5, "No high-quality pullback setup")

    def should_exit(self, df: pd.DataFrame) -> Dict[str, bool]:
        df = self.prepare(df)
        last = df.iloc[-1]
        return {
            "trend_reversal": last["Close"] < last["ema200"] and last["ema50"] < last["ema200"],
            "momentum_breakdown": last["macd_hist"] < 0,
        }
