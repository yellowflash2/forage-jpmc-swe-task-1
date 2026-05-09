from typing import Dict


def render_snapshot(stats: Dict) -> str:
    lines = [
        "=== Institutional Dip-Buying Bot Dashboard ===",
        f"Portfolio Value: ${stats['portfolio_value']:,.2f}",
        f"Exposure: {stats['exposure']:.2%}",
        f"Drawdown: {stats['drawdown']:.2%}",
        f"AI Confidence: {stats['ai_confidence']:.2f}",
        f"Trend Status: {stats['trend_status']}",
        f"Open Trades: {stats['open_trades']}",
        f"Risk Alerts: {stats['risk_alerts']}",
    ]
    return "\n".join(lines)
