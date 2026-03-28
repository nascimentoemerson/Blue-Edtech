from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal


SignalSide = Literal['buy', 'sell', 'hold']


@dataclass
class TradeSignal:
    side: SignalSide
    reason: str


class Strategy(ABC):
    @abstractmethod
    def generate_signal(self, klines: list) -> TradeSignal:
        raise NotImplementedError
