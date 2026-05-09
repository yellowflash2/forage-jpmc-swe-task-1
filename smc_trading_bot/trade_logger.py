import sqlite3


class TradeLogger:
    def __init__(self, db_path: str = "smc_trades.db"):
        self.db_path = db_path
        with sqlite3.connect(self.db_path) as c:
            c.execute(
                """CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY,
                symbol TEXT,timeframe TEXT,direction TEXT,htf_bias TEXT,bos_level REAL,fib_zone TEXT,
                entry_price REAL,stop_loss REAL,take_profit REAL,risk_pct REAL,r_multiple REAL,
                correlation_confirmation TEXT,entry_reason TEXT,exit_reason TEXT,win_loss TEXT
                )"""
            )

    def log(self, row: dict):
        with sqlite3.connect(self.db_path) as c:
            c.execute(
                """INSERT INTO trades(symbol,timeframe,direction,htf_bias,bos_level,fib_zone,entry_price,stop_loss,take_profit,
                risk_pct,r_multiple,correlation_confirmation,entry_reason,exit_reason,win_loss)
                VALUES(:symbol,:timeframe,:direction,:htf_bias,:bos_level,:fib_zone,:entry_price,:stop_loss,:take_profit,
                :risk_pct,:r_multiple,:correlation_confirmation,:entry_reason,:exit_reason,:win_loss)""",
                row,
            )
