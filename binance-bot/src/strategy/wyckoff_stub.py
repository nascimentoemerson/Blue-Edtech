from src.strategy.base import Strategy, TradeSignal


class WyckoffStrategyStub(Strategy):
    """Estratégia inicial (stub).

    Placeholder para futuras regras Wyckoff objetivas com confirmação por volume e estrutura.
    """

    def generate_signal(self, klines: list) -> TradeSignal:
        if len(klines) < 50:
            return TradeSignal(side='hold', reason='Dados insuficientes')

        closes = [float(k[4]) for k in klines[-20:]]
        avg_close = sum(closes) / len(closes)
        last_close = closes[-1]

        if last_close > avg_close * 1.003:
            return TradeSignal(side='buy', reason='Momentum acima da média (stub)')
        if last_close < avg_close * 0.997:
            return TradeSignal(side='sell', reason='Momentum abaixo da média (stub)')
        return TradeSignal(side='hold', reason='Sem vantagem estatística clara')
