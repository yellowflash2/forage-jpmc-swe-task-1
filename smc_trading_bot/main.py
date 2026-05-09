from .broker import Broker
from .config import BotConfig
from .correlation_filter import CorrelationFilter
from .dashboard import render
from .data_feed import DataFeed
from .liquidity_detector import LiquidityDetector
from .risk_manager import RiskManager
from .strategy import SMCStrategy
from .structure_detector import StructureDetector
from .trade_executor import TradeExecutor
from .trade_logger import TradeLogger


def run():
    cfg = BotConfig()
    feed = DataFeed()
    structure = StructureDetector()
    liquidity = LiquidityDetector()
    strategy = SMCStrategy()
    corr = CorrelationFilter()
    risk = RiskManager(cfg.risk_per_trade, cfg.max_daily_loss_r, cfg.max_weekly_loss_r)
    broker = Broker(cfg.mode)
    executor = TradeExecutor(broker)
    logger = TradeLogger()

    setups = trades = 0
    equity = 100_000
    for symbol in cfg.symbols:
        df_htf = feed.fetch(symbol, interval="1d")
        df_ltf = feed.fetch(symbol, interval="15m")
        if df_htf.empty or df_ltf.empty or not risk.can_trade():
            continue

        htf_bias = structure.detect_htf_trend(df_htf)
        structure_sig = structure.detect_bos_choch(df_ltf, cfg.min_displacement_atr)
        liq = liquidity.detect(df_ltf)
        price = float(df_ltf["Close"].iloc[-1])
        has_sweep = liquidity.liquidity_sweep(df_ltf, "buy" if structure_sig.trend == "bullish" else "sell")

        setup = strategy.build_setup(htf_bias, structure_sig, liq, price, has_fvg_or_ob=True, swept=has_sweep)
        if not setup:
            continue
        setups += 1

        correlated_ok = corr.confirm(symbol, setup.direction, {"DXY": -0.3, "VIX": -0.2}, cfg.correlation_map)
        if not correlated_ok:
            continue

        size = risk.position_size(equity, setup.entry, setup.stop)
        fill = executor.execute(symbol, setup, size)
        trades += 1
        logger.log(
            {
                "symbol": symbol,
                "timeframe": "15m",
                "direction": setup.direction,
                "htf_bias": htf_bias,
                "bos_level": structure_sig.bos_level,
                "fib_zone": setup.fib_zone,
                "entry_price": setup.entry,
                "stop_loss": setup.stop,
                "take_profit": setup.tp,
                "risk_pct": cfg.risk_per_trade,
                "r_multiple": 0.0,
                "correlation_confirmation": str(correlated_ok),
                "entry_reason": setup.reason,
                "exit_reason": "",
                "win_loss": "open",
            }
        )

    print(render({"mode": cfg.mode, "setups": setups, "trades": trades, "daily_r": risk.daily_r, "weekly_r": risk.weekly_r}))


if __name__ == "__main__":
    run()
