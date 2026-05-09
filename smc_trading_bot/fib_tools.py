from typing import Dict, Tuple


def fib_levels(range_low: float, range_high: float) -> Dict[str, float]:
    diff = range_high - range_low
    return {
        "0.62": range_high - diff * 0.62,
        "0.70": range_high - diff * 0.70,
        "0.79": range_high - diff * 0.79,
    }


def in_ote(price: float, levels: Dict[str, float], zone: Tuple[float, float] = (0.62, 0.70)) -> bool:
    z_high = levels[f"{zone[0]:.2f}"]
    z_low = levels[f"{zone[1]:.2f}"]
    return z_low <= price <= z_high
