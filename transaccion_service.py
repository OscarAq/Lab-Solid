from datetime import datetime
from oracle_repositorio import OracleRepositorio
from sms_gateway import SmsGateway
from cuenta import Cuenta

class TransaccionService:
    def __init__(self):
        self._repositorio = OracleRepositorio()
        self._sms = SmsGateway()

    def transferir(self, origen: Cuenta, destino: Cuenta, monto: float, tipo: str) -> None:
        # 1. Validación
        if monto <= 0:
            raise ValueError("Monto inválido")
        if monto > 5_000_000:
            raise ValueError("Supera el tope diario")

        # 2. Cálculo de la comisión
        if tipo == "MISMO_BANCO":
            comision = 0.0
        elif tipo == "OTRO_BANCO":
            comision = 7_500.0
        elif tipo == "INTERNACIONAL":
            comision = (monto * 0.03) + 25_000.0
        else:
            raise ValueError("Tipo de transferencia desconocido")

        # 3. Movimiento del dinero
        origen.retirar(monto + comision)
        destino.depositar(monto)

        # 4. Persistencia
        self._repositorio.guardar_transaccion(origen.get_numero(), destino.get_numero(), monto, comision)

        # 5. Comprobante
        print("===== BANCO ANDINO - COMPROBANTE =====")
        print(f"Origen: {origen.get_numero()}")
        print(f"Destino: {destino.get_numero()}")
        print(f"Monto: ${monto}")
        print(f"Comisión: ${comision}")
        print("=====================================")

        # 6. Notificación
        self._sms.enviar(origen.get_titular(), f"Transferiste ${monto} a la cuenta {destino.get_numero()}")

        # 7. Auditoría
        print(f"[AUDITORIA] {datetime.now()} {tipo} {origen.get_numero()}->{destino.get_numero()} ${monto}")