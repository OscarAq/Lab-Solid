from tipo_transferencia import TipoTransferencia


class TransferenciaLlave(TipoTransferencia):
    """R1 - Transferencia por llave (celular o cédula).

    Es inmediata y no cobra comisión. Para este laboratorio no se
    implementa la búsqueda de la cuenta a partir de la llave: solo se
    modela el tipo de transferencia, que es lo que afecta al cálculo de
    la comisión.
    """

    def calcular_comision(self, monto: float) -> float:
        return 0.0

    def nombre(self) -> str:
        return "LLAVE"
