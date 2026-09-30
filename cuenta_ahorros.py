from cuenta import Cuenta

class CuentaAhorros(Cuenta):
    def __init__(self, numero: str, titular: str, saldo_inicial: float):
        super().__init__(numero, titular, saldo_inicial)