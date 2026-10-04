from abc import ABC, abstractmethod


class ProductoConCuota(ABC):
    @abstractmethod
    def pagar_cuota(self, monto: float) -> None:
        pass