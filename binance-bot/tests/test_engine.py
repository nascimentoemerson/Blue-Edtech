from src.core.engine import TradingContext, TradingEngine
from src.execution.executor import OrderExecutor
from src.risk.manager import RiskManager
from src.strategy.base import Strategy, TradeSignal


class FakeDataClient:
    def get_klines(self, symbol: str, interval: str = '15m', limit: int = 200):
        _ = symbol, interval, limit
        return [[0, 0, 0, 0, '100', 0] for _ in range(60)]

    def get_last_price(self, symbol: str) -> float:
        _ = symbol
        return 100.0


class AlwaysBuyStrategy(Strategy):
    def generate_signal(self, klines: list) -> TradeSignal:
        _ = klines
        return TradeSignal(side='buy', reason='test-buy')


class AlwaysHoldStrategy(Strategy):
    def generate_signal(self, klines: list) -> TradeSignal:
        _ = klines
        return TradeSignal(side='hold', reason='test-hold')


def test_engine_executes_paper_order() -> None:
    engine = TradingEngine(
        strategy=AlwaysBuyStrategy(),
        risk_manager=RiskManager(risk_per_trade=0.01, max_daily_loss=0.02, max_trades_per_day=8),
        executor=OrderExecutor(mode='paper'),
        data_client=FakeDataClient(),
    )

    result = engine.run_once(
        TradingContext(
            symbol='BTCUSDT',
            market='futures',
            equity=1000,
            daily_pnl_pct=0,
            trades_today=0,
        )
    )

    assert result['status'] == 'executed'
    assert result['order']['status'] == 'simulated'


def test_engine_returns_no_trade_on_hold_signal() -> None:
    engine = TradingEngine(
        strategy=AlwaysHoldStrategy(),
        risk_manager=RiskManager(risk_per_trade=0.01, max_daily_loss=0.02, max_trades_per_day=8),
        executor=OrderExecutor(mode='paper'),
        data_client=FakeDataClient(),
    )

    result = engine.run_once(
        TradingContext(
            symbol='BTCUSDT',
            market='spot',
            equity=1000,
            daily_pnl_pct=0,
            trades_today=0,
        )
    )

    assert result == {'status': 'no_trade', 'reason': 'test-hold'}
