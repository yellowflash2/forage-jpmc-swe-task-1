from typing import Dict


class CorrelationFilter:
    def confirm(self, symbol: str, direction: str, corr_prices: Dict[str, float], corr_map: Dict[str, Dict[str, str]]) -> bool:
        relations = corr_map.get(symbol, {})
        for asset, kind in relations.items():
            move = corr_prices.get(asset, 0.0)
            if direction == "buy" and kind == "inverse" and move > 0.5:
                return False
            if direction == "sell" and kind == "inverse" and move < -0.5:
                return False
        return True
