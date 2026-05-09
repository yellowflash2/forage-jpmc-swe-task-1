import yfinance as yf


class DataFeed:
    def fetch(self, symbol: str, interval: str = "1h", period: str = "180d"):
        ticker = symbol if symbol.startswith("^") else symbol
        return yf.download(ticker, interval=interval, period=period, progress=False, auto_adjust=True)
