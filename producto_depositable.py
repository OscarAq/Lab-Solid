from abc import ABC, abstractmethod


class ProductoDepositable(ABC):
    @abstractmethod
    def depositar(self, monto: float) -> None:
        pass