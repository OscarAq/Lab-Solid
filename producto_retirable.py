from abc import ABC, abstractmethod


class ProductoRetirable(ABC):
    @abstractmethod
    def retirar(self, monto: float) -> None:
        pass