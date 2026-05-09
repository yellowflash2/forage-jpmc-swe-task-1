# Trading Bot Architectures

This repository now includes two modular bots:

1. `bot/` - long-term index dip-buying portfolio bot.
2. `smc_trading_bot/` - professional Liquidity/SMC trend-following bot based on HTF bias, BOS/BMS, displacement, retracement, OTE, liquidity confluence, and correlation filtering.

## SMC Trading Bot Structure

```
/smc_trading_bot
    main.py
    config.py
    data_feed.py
    broker.py
    strategy.py
    structure_detector.py
    liquidity_detector.py
    fib_tools.py
    correlation_filter.py
    risk_manager.py
    trade_executor.py
    trade_logger.py
    backtester.py
    dashboard.py
```

## SMC Strategy Highlights

- Multi-timeframe logic (Daily/4H bias, 1H/15M structure, 5M/1M entries).
- BOS/BMS + displacement required before retracement entries.
- OTE zone validation (0.62-0.70, optional 0.79).
- Liquidity integration: PMH/PML, PWH/PWL, PDH/PDL, equal highs/lows, liquidity sweep checks.
- Correlation filters (DXY/VIX for US indices, configurable per symbol).
- Risk guardrails: 0.5-1% style risk per trade, daily/weekly loss caps, R-based sizing hooks.
- Backtest-ready metrics: win rate, profit factor, max drawdown, average R.

## Install / Run

```bash
pip install -r requirements.txt
python -m smc_trading_bot.main
```

`broker.py` is intentionally adapter-friendly for MetaTrader 5 integration.
