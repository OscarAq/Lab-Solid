from producto_bancario import ProductoBancario
from producto_retirable import ProductoRetirable
from producto_con_intereses import ProductoConIntereses
from producto_con_cuota import ProductoConCuota


class TarjetaCredito(
    ProductoBancario,
    ProductoRetirable,
    ProductoConIntereses,
    ProductoConCuota
):
    def __init__(self, cupo: float):
        self._cupo = cupo
        self._deuda = 0.0

    def retirar(self, monto: float) -> None:
        if self._deuda + monto > self._cupo:
            raise RuntimeError("Cupo insuficiente")
        self._deuda += monto

    def calcular_intereses(self) -> float:
        return self._deuda * 0.028

    def pagar_cuota(self, monto: float) -> None:
        self._deuda -= monto

    def generar_extracto(self) -> str:
        return f"Tarjeta - deuda: ${self._deuda}"