from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    binance_api_key: str = ''
    binance_api_secret: str = ''
    binance_testnet: bool = True

    risk_per_trade: float = 0.01
    max_daily_loss: float = 0.02
    max_trades_per_day: int = 8


settings = Settings()
