from dataclasses import dataclass
import pandas as pd


@dataclass
class StructureSignal:
    trend: str
    bos_level: float
    choch: bool
    displacement: bool
    range_low: float
    range_high: float


class StructureDetector:
    def detect_htf_trend(self, df: pd.DataFrame) -> str:
        ema50 = df["Close"].ewm(span=50, adjust=False).mean().iloc[-1]
        ema200 = df["Close"].ewm(span=200, adjust=False).mean().iloc[-1]
        close = df["Close"].iloc[-1]
        if close > ema200 and ema50 > ema200:
            return "bullish"
        if close < ema200 and ema50 < ema200:
            return "bearish"
        return "neutral"

    def detect_bos_choch(self, df: pd.DataFrame, min_displacement_atr: float = 1.2) -> StructureSignal:
        atr = (df["High"] - df["Low"]).rolling(14).mean().iloc[-1]
        last = df.iloc[-1]
        prev = df.iloc[-2]
        bullish_bos = last["High"] > df["High"].iloc[-20:-1].max()
        bearish_bos = last["Low"] < df["Low"].iloc[-20:-1].min()
        disp = abs(last["Close"] - last["Open"]) > atr * min_displacement_atr
        choch = (prev["Close"] < prev["Open"] and last["Close"] > last["Open"]) or (
            prev["Close"] > prev["Open"] and last["Close"] < last["Open"]
        )

        if bullish_bos:
            return StructureSignal("bullish", float(last["High"]), choch, disp, float(df["Low"].iloc[-10:-1].min()), float(last["High"]))
        if bearish_bos:
            return StructureSignal("bearish", float(last["Low"]), choch, disp, float(last["Low"]), float(df["High"].iloc[-10:-1].max()))
        return StructureSignal("neutral", float(last["Close"]), choch, False, float(df["Low"].iloc[-10:-1].min()), float(df["High"].iloc[-10:-1].max()))
