from dataclasses import dataclass


@dataclass
class AccountSnapshot:
    equity: float
    daily_pnl_pct: float
    trades_today: int


class RiskManager:
    def __init__(self, risk_per_trade: float, max_daily_loss: float, max_trades_per_day: int) -> None:
        if risk_per_trade <= 0:
            raise ValueError('risk_per_trade deve ser maior que zero')
        if max_daily_loss <= 0:
            raise ValueError('max_daily_loss deve ser maior que zero')
        if max_trades_per_day <= 0:
            raise ValueError('max_trades_per_day deve ser maior que zero')

        self.risk_per_trade = risk_per_trade
        self.max_daily_loss = max_daily_loss
        self.max_trades_per_day = max_trades_per_day

    def can_trade(self, account: AccountSnapshot) -> tuple[bool, str]:
        if account.daily_pnl_pct <= -self.max_daily_loss:
            return False, 'Limite de perda diária atingido'
        if account.trades_today >= self.max_trades_per_day:
            return False, 'Limite de trades diário atingido'
        return True, 'OK'

    def calculate_position_size(self, equity: float, entry_price: float, stop_price: float) -> float:
        if equity <= 0:
            return 0.0
        risk_amount = equity * self.risk_per_trade
        stop_distance = abs(entry_price - stop_price)
        if stop_distance <= 0:
            return 0.0
        return risk_amount / stop_distance
