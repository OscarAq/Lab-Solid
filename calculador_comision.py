from tipo_transferencia import TipoTransferencia


class CalculadorComision:

    def calcular(self, monto: float, tipo: TipoTransferencia) -> float:
        return tipo.calcular_comision(monto)