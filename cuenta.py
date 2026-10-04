class Cuenta:
    def __init__(self, numero: str, titular: str, saldo_inicial: float):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo_inicial

    def get_numero(self) -> str:
        return self._numero

    def get_titular(self) -> str:
        return self._titular

    def get_saldo(self) -> float:
        return self._saldo

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto inválido")
        self._saldo += monto

