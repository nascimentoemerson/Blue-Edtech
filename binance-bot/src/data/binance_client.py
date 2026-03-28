from binance.client import Client

from src.config.settings import settings


class BinanceDataClient:
    def __init__(self) -> None:
        self.client = Client(settings.binance_api_key, settings.binance_api_secret, testnet=settings.binance_testnet)

    def get_last_price(self, symbol: str) -> float:
        ticker = self.client.get_symbol_ticker(symbol=symbol)
        return float(ticker['price'])

    def get_klines(self, symbol: str, interval: str = Client.KLINE_INTERVAL_15MINUTE, limit: int = 200):
        return self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
