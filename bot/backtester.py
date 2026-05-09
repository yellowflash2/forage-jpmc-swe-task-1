from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd


@dataclass
class BacktestResult:
    cagr: float
    sharpe: float
    max_drawdown: float
    win_rate: float


class Backtester:
    def run(self, equity_curve: pd.Series, trades: pd.DataFrame) -> BacktestResult:
        returns = equity_curve.pct_change().dropna()
        years = max((equity_curve.index[-1] - equity_curve.index[0]).days / 365.25, 1 / 365.25)
        cagr = (equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (1 / years) - 1
        sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0.0
        rolling_max = equity_curve.cummax()
        max_dd = ((equity_curve - rolling_max) / rolling_max).min()
        win_rate = (trades["pnl"] > 0).mean() if not trades.empty else 0.0
        return BacktestResult(float(cagr), float(sharpe), float(abs(max_dd)), float(win_rate))

    def monte_carlo(self, returns: pd.Series, n_sims: int = 1000, horizon_days: int = 252) -> Dict[str, float]:
        sims = []
        for _ in range(n_sims):
            path = np.random.choice(returns.values, size=horizon_days, replace=True)
            sims.append(np.prod(1 + path) - 1)
        return {
            "p05": float(np.percentile(sims, 5)),
            "p50": float(np.percentile(sims, 50)),
            "p95": float(np.percentile(sims, 95)),
        }
