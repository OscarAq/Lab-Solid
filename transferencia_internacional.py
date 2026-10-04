from tipo_transferencia import TipoTransferencia


class TransferenciaInternacional(TipoTransferencia):

    def calcular_comision(self, monto: float) -> float:
        return (monto * 0.03) + 25_000.0

    def nombre(self) -> str:
        return "INTERNACIONAL"