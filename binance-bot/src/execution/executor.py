from dataclasses import dataclass


@dataclass
class OrderRequest:
    symbol: str
    side: str
    quantity: float
    market: str  # spot | futures


class OrderExecutor:
    def __init__(self, mode: str = 'paper') -> None:
        valid_modes = {'paper', 'live'}
        if mode not in valid_modes:
            raise ValueError(f'mode inválido: {mode}. Use um de {valid_modes}')
        self.mode = mode

    def execute(self, order: OrderRequest) -> dict:
        if order.quantity <= 0:
            return {'status': 'rejected', 'reason': 'Quantidade deve ser maior que zero'}
        if order.side not in {'buy', 'sell'}:
            return {'status': 'rejected', 'reason': "Lado da ordem precisa ser 'buy' ou 'sell'"}

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
