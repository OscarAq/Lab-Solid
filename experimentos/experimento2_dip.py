from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from cuenta_ahorros import CuentaAhorros
from transaccion_service import TransaccionService
from validador_transferencia import ValidadorTransferencia
from calculador_comision import CalculadorComision
from generador_comprobante import GeneradorComprobante
from auditor_transferencia import AuditorTransferencia
from transferencia_mismo_banco import TransferenciaMismoBanco


class FakeRepositorio:
    def __init__(self):
        self.transacciones = []

    def guardar_transaccion(
        self,
        origen,
        destino,
        monto,
        comision
    ):
        self.transacciones.append({
            "origen": origen,
            "destino": destino,
            "monto": monto,
            "comision": comision
        })


class FakeNotificador:
    def __init__(self):
        self.notificaciones = []

    def enviar(self, destinatario, mensaje):
        self.notificaciones.append({
            "destinatario": destinatario,
            "mensaje": mensaje
        })


def main():
    origen = CuentaAhorros("001-1", "Ana", 2_000_000)
    destino = CuentaAhorros("001-2", "Luis", 500_000)

    repositorio = FakeRepositorio()
    notificador = FakeNotificador()

    servicio = TransaccionService(
        repositorio,
        notificador,
        ValidadorTransferencia(),
        CalculadorComision(),
        GeneradorComprobante(),
        AuditorTransferencia()
    )

    servicio.transferir(
        origen,
        destino,
        150_000,
        TransferenciaMismoBanco()
    )

    print("\n===== RESULTADO DE LA PRUEBA =====")

    print(f"Saldo Ana: ${origen.get_saldo()}")
    print(f"Saldo Luis: ${destino.get_saldo()}")

    print(f"Transacciones guardadas: {len(repositorio.transacciones)}")
    print(f"Notificaciones enviadas: {len(notificador.notificaciones)}")

    print("\nTransacción:")
    print(repositorio.transacciones[0])

    print("\nNotificación:")
    print(notificador.notificaciones[0])


if __name__ == "__main__":
    main()