from tipo_transferencia import TipoTransferencia


class TransferenciaMismoBanco(TipoTransferencia):

    def calcular_comision(self, monto: float) -> float:
        return 0.0

    def nombre(self) -> str:
        return "MISMO_BANCO"