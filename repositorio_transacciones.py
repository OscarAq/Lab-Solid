from abc import ABC, abstractmethod


class RepositorioTransacciones(ABC):

    @abstractmethod
    def guardar_transaccion(
        self,
        origen: str,
        destino: str,
        monto: float,
        comision: float
    ) -> None:
        pass