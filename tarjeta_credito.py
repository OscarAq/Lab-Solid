from producto_bancario import ProductoBancario

class TarjetaCredito(ProductoBancario):
    def __init__(self, cupo: float):
        self._cupo = cupo
        self._deuda = 0.0

    def depositar(self, monto: float) -> None:
        pass  # No aplica

    def retirar(self, monto: float) -> None:  # Avance en efectivo
        if self._deuda + monto > self._cupo:
            raise RuntimeError("Cupo insuficiente")
        self._deuda += monto

    def calcular_intereses(self) -> float:
        return self._deuda * 0.028

    def pagar_cuota(self, monto: float) -> None:
        self._deuda -= monto

    def generar_extracto(self) -> str:
        return f"Tarjeta - deuda: ${self._deuda}"