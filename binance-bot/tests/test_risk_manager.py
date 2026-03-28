import pytest

from src.risk.manager import AccountSnapshot, RiskManager


def test_blocks_when_daily_loss_limit_hit() -> None:
    manager = RiskManager(risk_per_trade=0.01, max_daily_loss=0.02, max_trades_per_day=5)
    allowed, reason = manager.can_trade(AccountSnapshot(equity=1000, daily_pnl_pct=-0.02, trades_today=0))

    assert allowed is False
    assert reason == 'Limite de perda diária atingido'


def test_calculate_position_size() -> None:
    manager = RiskManager(risk_per_trade=0.01, max_daily_loss=0.02, max_trades_per_day=5)
    size = manager.calculate_position_size(equity=1000, entry_price=100, stop_price=99)

    assert size == 10


@pytest.mark.parametrize(
    'risk_per_trade,max_daily_loss,max_trades_per_day',
    [
        (0, 0.02, 5),
        (0.01, 0, 5),
        (0.01, 0.02, 0),
    ],
)
def test_invalid_risk_manager_config_raises(
    risk_per_trade: float,
    max_daily_loss: float,
    max_trades_per_day: int,
) -> None:
    with pytest.raises(ValueError):
        RiskManager(
            risk_per_trade=risk_per_trade,
            max_daily_loss=max_daily_loss,
            max_trades_per_day=max_trades_per_day,
        )
