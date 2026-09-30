from abc import ABC, abstractmethod

class ProductoBancario(ABC):
    @abstractmethod
    def depositar(self, monto: float) -> None:
        pass

    @abstractmethod
    def retirar(self, monto: float) -> None:
        pass

    @abstractmethod
    def calcular_intereses(self) -> float:
        pass

    @abstractmethod
    def pagar_cuota(self, monto: float) -> None:
        pass

    @abstractmethod
    def generar_extracto(self) -> str:
        pass