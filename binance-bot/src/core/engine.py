from src.data.binance_client import BinanceDataClient
from src.execution.executor import OrderExecutor, OrderRequest
from src.risk.manager import RiskManager, AccountSnapshot
from src.strategy.base import Strategy


class TradingEngine:
    def __init__(self, strategy: Strategy, risk_manager: RiskManager, executor: OrderExecutor) -> None:
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.executor = executor
        self.data_client = BinanceDataClient()

    def run_once(self, symbol: str, market: str, equity: float, daily_pnl_pct: float, trades_today: int) -> dict:
        account = AccountSnapshot(equity=equity, daily_pnl_pct=daily_pnl_pct, trades_today=trades_today)
        allowed, reason = self.risk_manager.can_trade(account)
        if not allowed:
            return {'status': 'blocked', 'reason': reason}

        klines = self.data_client.get_klines(symbol=symbol)
        signal = self.strategy.generate_signal(klines)

        if signal.side == 'hold':
            return {'status': 'no_trade', 'reason': signal.reason}

        entry_price = self.data_client.get_last_price(symbol)
        stop_price = entry_price * (0.99 if signal.side == 'buy' else 1.01)
        quantity = self.risk_manager.calculate_position_size(equity=equity, entry_price=entry_price, stop_price=stop_price)

        if quantity <= 0:
            return {'status': 'no_trade', 'reason': 'Tamanho de posição inválido'}

        order = OrderRequest(symbol=symbol, side=signal.side, quantity=round(quantity, 6), market=market)
        execution_result = self.executor.execute(order)

        return {
            'status': 'executed' if execution_result.get('status') == 'simulated' else execution_result.get('status'),
            'signal': signal.reason,
            'order': execution_result,
        }
