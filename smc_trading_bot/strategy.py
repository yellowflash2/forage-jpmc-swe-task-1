from dataclasses import dataclass
from typing import Optional

from .fib_tools import fib_levels, in_ote


@dataclass
class TradeSetup:
    direction: str
    entry: float
    stop: float
    tp: float
    fib_zone: str
    reason: str


class SMCStrategy:
    def build_setup(self, htf_bias: str, structure, liq, price: float, has_fvg_or_ob: bool, swept: bool) -> Optional[TradeSetup]:
        if htf_bias == "neutral" or structure.trend == "neutral" or not structure.displacement:
            return None
        if htf_bias != structure.trend:
            return None

        levels = fib_levels(structure.range_low, structure.range_high)
        if structure.trend == "bullish":
            valid = in_ote(price, levels) and (has_fvg_or_ob or swept)
            if not valid:
                return None
            stop = min(structure.range_low, liq.pdl)
            tp = max(structure.range_high, liq.pmh)
            return TradeSetup("buy", price, stop, tp, "0.62-0.70", "HTF bullish + BOS + displacement + OTE")

        valid = in_ote(price, levels) and (has_fvg_or_ob or swept)
        if not valid:
            return None
        stop = max(structure.range_high, liq.pdh)
        tp = min(structure.range_low, liq.pml)
        return TradeSetup("sell", price, stop, tp, "0.62-0.70", "HTF bearish + BOS + displacement + OTE")
