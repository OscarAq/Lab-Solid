from abc import ABC, abstractmethod


class TipoTransferencia(ABC):

    @abstractmethod
    def calcular_comision(self, monto: float) -> float:
        pass

    @abstractmethod
    def nombre(self) -> str:
        pass