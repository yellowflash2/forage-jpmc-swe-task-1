import sqlite3
from pathlib import Path
from typing import Dict


class TradeLogger:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_date TEXT,
                    exit_date TEXT,
                    symbol TEXT,
                    position_size REAL,
                    pnl REAL,
                    entry_reason TEXT,
                    exit_reason TEXT,
                    ai_confidence REAL
                )
                """
            )

    def log_trade(self, trade: Dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO trades (entry_date, exit_date, symbol, position_size, pnl, entry_reason, exit_reason, ai_confidence)
                VALUES (:entry_date, :exit_date, :symbol, :position_size, :pnl, :entry_reason, :exit_reason, :ai_confidence)
                """,
                trade,
            )
