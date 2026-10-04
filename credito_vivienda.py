from producto_bancario import ProductoBancario
from producto_con_intereses import ProductoConIntereses
from producto_con_cuota import ProductoConCuota


class CreditoVivienda(
    ProductoBancario,
    ProductoConIntereses,
    ProductoConCuota
):
    def __init__(self, valor_prestamo: float):
        self._saldo_pendiente = valor_prestamo

    def calcular_intereses(self) -> float:
        return self._saldo_pendiente * 0.011

    def pagar_cuota(self, monto: float) -> None:
        self._saldo_pendiente -= monto

    def generar_extracto(self) -> str:
        return f"Crédito vivienda - pendiente: ${self._saldo_pendiente}"