from datetime import date
from cuenta import Cuenta

class CDT(Cuenta):
    def __init__(self, numero: str, titular: str, monto: float, vencimiento: date):
        super().__init__(numero, titular, monto)
        self._vencimiento = vencimiento

    def retirar(self, monto: float) -> None:
        if date.today() < self._vencimiento:
            raise RuntimeError("Un CDT no permite retiros antes del vencimiento")
        super().retirar(monto)