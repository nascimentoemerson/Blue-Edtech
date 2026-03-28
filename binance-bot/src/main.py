import argparse
from pprint import pprint

from src.config.settings import settings
from src.core.engine import TradingEngine
from src.execution.executor import OrderExecutor
from src.risk.manager import RiskManager
from src.strategy.wyckoff_stub import WyckoffStrategyStub


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Binance Trading Bot MVP')
    parser.add_argument('--symbol', default='BTCUSDT')
    parser.add_argument('--market', choices=['spot', 'futures'], default='futures')
    parser.add_argument('--mode', choices=['paper', 'live'], default='paper')
    parser.add_argument('--equity', type=float, default=1000.0)
    parser.add_argument('--daily-pnl-pct', type=float, default=0.0)
    parser.add_argument('--trades-today', type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    strategy = WyckoffStrategyStub()
    risk_manager = RiskManager(
        risk_per_trade=settings.risk_per_trade,
        max_daily_loss=settings.max_daily_loss,
        max_trades_per_day=settings.max_trades_per_day,
    )
    executor = OrderExecutor(mode=args.mode)
    engine = TradingEngine(strategy=strategy, risk_manager=risk_manager, executor=executor)

    result = engine.run_once(
        symbol=args.symbol,
        market=args.market,
        equity=args.equity,
        daily_pnl_pct=args.daily_pnl_pct,
        trades_today=args.trades_today,
    )
    pprint(result)


if __name__ == '__main__':
    main()
