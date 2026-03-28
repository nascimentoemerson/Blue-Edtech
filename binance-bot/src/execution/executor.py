from dataclasses import dataclass


@dataclass
class OrderRequest:
    symbol: str
    side: str
    quantity: float
    market: str  # spot | futures


class OrderExecutor:
    def __init__(self, mode: str = 'paper') -> None:
        self.mode = mode

    def execute(self, order: OrderRequest) -> dict:
        if self.mode == 'paper':
            return {
                'status': 'simulated',
                'symbol': order.symbol,
                'side': order.side,
                'quantity': order.quantity,
                'market': order.market,
            }

        # TODO: ligar execução real Binance (spot/futures) com validações extras.
        return {'status': 'not_implemented_live_mode'}
