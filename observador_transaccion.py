from abc import ABC, abstractmethod
from cuenta import Cuenta
from cuenta_retirable import CuentaRetirable


class ObservadorTransaccion(ABC):
    """R4 - Observador de transacciones exitosas.

    Abstracción que permite "engancharse" al flujo de una transferencia
    después de que esta se completa con éxito, sin tocar el cálculo central
    de TransaccionService. Cualquier sistema que deba reaccionar a una
    transacción exitosa (antifraude, metricas, etc.) implementa esta
    interfaz y se inyecta como observador.
    """

    @abstractmethod
    def registrar_transaccion(
        self,
        origen: CuentaRetirable,
        destino: Cuenta,
        monto: float,
        comision: float,
        tipo: str,
    ) -> None:
        pass
