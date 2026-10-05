from datetime import date
from cuenta_retirable import CuentaRetirable


class CuentaInfantil(CuentaRetirable):
    """R2 - Cuenta para menores de edad.

    Recibe depósitos sin límite (heredado de Cuenta), pero sus retiros no
    pueden superar $200.000 en un mismo día. Al heredar de CuentaRetirable
    puede usarse como origen de transferencias y se le puede cobrar la
    cuota de manejo como a cualquier otra cuenta retirable.
    """

    LIMITE_DIARIO = 200_000

    def __init__(self, numero: str, titular: str, saldo_inicial: float):
        super().__init__(numero, titular, saldo_inicial)
        self._retirado_hoy = 0.0
        self._fecha_retiro = date.today()

    def retirar(self, monto: float) -> None:
        hoy = date.today()
        if hoy != self._fecha_retiro:
            self._fecha_retiro = hoy
            self._retirado_hoy = 0.0

        if self._retirado_hoy + monto > self.LIMITE_DIARIO:
            raise RuntimeError(
                "Supera el límite de retiro diario de la cuenta infantil"
            )

        # Delega la validación de saldo y el descuento en CuentaRetirable.
        # Si el saldo es insuficiente, se lanza la excepción antes de
        # acumular el retiro del día, por lo que el estado no cambia.
        super().retirar(monto)
        self._retirado_hoy += monto
