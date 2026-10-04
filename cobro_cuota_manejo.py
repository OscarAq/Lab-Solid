from typing import List
# pyrefly: ignore [missing-import]
from cuenta_retirable import CuentaRetirable
class CobroCuotaManejo:
    CUOTA = 12_900.0

    def cobrar_mensual(self, cuentas: List[Cuenta]) -> None:
        for cuenta in cuentas:
            cuenta.retirar(self.CUOTA)
            print(f"Cuota de manejo cobrada a {cuenta.get_numero()}")