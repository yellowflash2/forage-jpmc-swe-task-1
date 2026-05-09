import pandas as pd


def summarize(trades: pd.DataFrame) -> dict:
    if trades.empty:
        return {"win_rate": 0, "profit_factor": 0, "max_drawdown": 0, "average_r": 0}
    wins = trades[trades["r_multiple"] > 0]
    losses = trades[trades["r_multiple"] < 0]
    gross_profit = wins["r_multiple"].sum()
    gross_loss = abs(losses["r_multiple"].sum()) or 1e-8
    equity = trades["r_multiple"].cumsum()
    dd = (equity - equity.cummax()).min()
    return {
        "win_rate": float((trades["r_multiple"] > 0).mean()),
        "profit_factor": float(gross_profit / gross_loss),
        "max_drawdown": float(abs(dd)),
        "average_r": float(trades["r_multiple"].mean()),
    }
