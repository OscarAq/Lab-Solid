from cuenta import Cuenta
from cuenta_retirable import CuentaRetirable
from validador_transferencia import ValidadorTransferencia
from calculador_comision import CalculadorComision
from generador_comprobante import GeneradorComprobante
from auditor_transferencia import AuditorTransferencia
from tipo_transferencia import TipoTransferencia
from repositorio_transacciones import RepositorioTransacciones
from notificador import Notificador


class TransaccionService:
    def __init__(self,repositorio: RepositorioTransacciones,notificador: Notificador,validador: ValidadorTransferencia,calculador_comision: CalculadorComision,comprobante: GeneradorComprobante,auditor: AuditorTransferencia):
        self._repositorio = repositorio
        self._notificador = notificador
        self._validador = validador
        self._calculador_comision = calculador_comision
        self._comprobante = comprobante
        self._auditor = auditor

    def transferir(self,origen: CuentaRetirable,destino: Cuenta,monto: float,tipo: TipoTransferencia) -> None:

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
        self._notificador.enviar(
            origen.get_titular(),
            f"Transferiste ${monto} a la cuenta {destino.get_numero()}"
        )

        # 7. Auditoría
        self._auditor.registrar(
            tipo.nombre(),
            origen,
            destino,
            monto
        )