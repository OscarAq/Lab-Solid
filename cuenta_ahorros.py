from cuenta_retirable import CuentaRetirable


class CuentaAhorros(CuentaRetirable):

    def __init__(self,numero: str,titular: str,saldo_inicial: float):
        super().__init__(numero, titular, saldo_inicial)