from dataclasses import dataclass
import pandas as pd


@dataclass
class LiquidityMap:
    pmh: float
    pml: float
    pwh: float
    pwl: float
    pdh: float
    pdl: float
    equal_highs: bool
    equal_lows: bool


class LiquidityDetector:
    def detect(self, df: pd.DataFrame) -> LiquidityMap:
        return LiquidityMap(
            pmh=float(df["High"].iloc[-22:].max()),
            pml=float(df["Low"].iloc[-22:].min()),
            pwh=float(df["High"].iloc[-5:].max()),
            pwl=float(df["Low"].iloc[-5:].min()),
            pdh=float(df["High"].iloc[-2]),
            pdl=float(df["Low"].iloc[-2]),
            equal_highs=abs(df["High"].iloc[-1] - df["High"].iloc[-3]) / df["High"].iloc[-1] < 0.001,
            equal_lows=abs(df["Low"].iloc[-1] - df["Low"].iloc[-3]) / df["Low"].iloc[-1] < 0.001,
        )

    def liquidity_sweep(self, df: pd.DataFrame, side: str) -> bool:
        if side == "buy":
            return df["Low"].iloc[-1] < df["Low"].iloc[-6:-1].min() and df["Close"].iloc[-1] > df["Open"].iloc[-1]
        return df["High"].iloc[-1] > df["High"].iloc[-6:-1].max() and df["Close"].iloc[-1] < df["Open"].iloc[-1]
