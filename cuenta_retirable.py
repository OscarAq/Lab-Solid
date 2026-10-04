from cuenta import Cuenta


class CuentaRetirable(Cuenta):

    def retirar(self, monto: float) -> None:
        if monto > self._saldo:
            raise RuntimeError("Saldo insuficiente")

        self._saldo -= monto