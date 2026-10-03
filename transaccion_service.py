from oracle_repositorio import OracleRepositorio
from sms_gateway import SmsGateway
from cuenta import Cuenta

from validador_transferencia import ValidadorTransferencia
from calculador_comision import CalculadorComision
from generador_comprobante import GeneradorComprobante
from auditor_transferencia import AuditorTransferencia


class TransaccionService:
    def __init__(self):
        self._repositorio = OracleRepositorio()
        self._sms = SmsGateway()

        self._validador = ValidadorTransferencia()
        self._calculador_comision = CalculadorComision()
        self._comprobante = GeneradorComprobante()
        self._auditor = AuditorTransferencia()

    def transferir(
        self,
        origen: Cuenta,
        destino: Cuenta,
        monto: float,
        tipo: str
    ) -> None:

        # 1. Validación
        self._validador.validar(monto)

        # 2. Cálculo de la comisión
        comision = self._calculador_comision.calcular(monto, tipo)

        # 3. Movimiento del dinero
        origen.retirar(monto + comision)
        destino.depositar(monto)

        # 4. Persistencia
        self._repositorio.guardar_transaccion(
            origen.get_numero(),
            destino.get_numero(),
            monto,
            comision
        )

        # 5. Comprobante
        self._comprobante.generar(
            origen,
            destino,
            monto,
            comision
        )

        # 6. Notificación
        self._sms.enviar(
            origen.get_titular(),
            f"Transferiste ${monto} a la cuenta {destino.get_numero()}"
        )

        # 7. Auditoría
        self._auditor.registrar(
            tipo,
            origen,
            destino,
            monto
        )