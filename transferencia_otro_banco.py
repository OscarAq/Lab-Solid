from tipo_transferencia import TipoTransferencia


class TransferenciaOtroBanco(TipoTransferencia):

    def calcular_comision(self, monto: float) -> float:
        return 7_500.0

    def nombre(self) -> str:
        return "OTRO_BANCO"