from dataclasses import dataclass
from typing import Protocol

from src.execution.executor import OrderExecutor, OrderRequest
from src.risk.manager import AccountSnapshot, RiskManager
from src.strategy.base import Strategy


class MarketDataProvider(Protocol):
    def get_klines(self, symbol: str, interval: str = '15m', limit: int = 200):
        ...

    def get_last_price(self, symbol: str) -> float:
        ...


@dataclass
class TradingContext:
    symbol: str
    market: str
    equity: float
    daily_pnl_pct: float
    trades_today: int


class TradingEngine:
    def __init__(
        self,
        strategy: Strategy,
        risk_manager: RiskManager,
        executor: OrderExecutor,
        data_client: MarketDataProvider,
    ) -> None:
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.executor = executor
        self.data_client = data_client

    def run_once(self, context: TradingContext) -> dict:
        account = AccountSnapshot(
            equity=context.equity,
            daily_pnl_pct=context.daily_pnl_pct,
            trades_today=context.trades_today,
        )
        allowed, reason = self.risk_manager.can_trade(account)
        if not allowed:
            return {'status': 'blocked', 'reason': reason}

        klines = self.data_client.get_klines(symbol=context.symbol)
        signal = self.strategy.generate_signal(klines)

        if signal.side == 'hold':
            return {'status': 'no_trade', 'reason': signal.reason}

        entry_price = self.data_client.get_last_price(context.symbol)
        stop_price = entry_price * (0.99 if signal.side == 'buy' else 1.01)
        quantity = self.risk_manager.calculate_position_size(
            equity=context.equity,
            entry_price=entry_price,
            stop_price=stop_price,
        )

        if quantity <= 0:
            return {'status': 'no_trade', 'reason': 'Tamanho de posição inválido'}

        order = OrderRequest(
            symbol=context.symbol,
            side=signal.side,
            quantity=round(quantity, 6),
            market=context.market,
        )
        execution_result = self.executor.execute(order)

        return {
            'status': 'executed' if execution_result.get('status') == 'simulated' else execution_result.get('status'),
            'signal': signal.reason,
            'order': execution_result,
        }
