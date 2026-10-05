from datetime import date, timedelta
from cuenta_ahorros import CuentaAhorros
from cuenta_infantil import CuentaInfantil
from cdt import CDT
from transaccion_service import TransaccionService
from cobro_cuota_manejo import CobroCuotaManejo
from tarjeta_credito import TarjetaCredito
from credito_vivienda import CreditoVivienda
from transferencia_otro_banco import TransferenciaOtroBanco
from transferencia_llave import TransferenciaLlave
from postgres_repositorio import PostgresRepositorio
from sms_gateway import SmsGateway
from push_notifier import PushNotifier
from notificador_compuesto import NotificadorCompuesto
from antifraude_service import AntifraudeService
from validador_transferencia import ValidadorTransferencia
from calculador_comision import CalculadorComision
from generador_comprobante import GeneradorComprobante
from auditor_transferencia import AuditorTransferencia


def main():
    ana = CuentaAhorros("001-1", "Ana", 2_000_000)
    luis = CuentaAhorros("001-2", "Luis", 500_000)

    cdt_ana = CDT("CDT-9", "Ana", 10_000_000, date.today() + timedelta(days=180))

    # --- Armado de dependencias (inyección desde main) ---
    # R5: se guarda en PostgreSQL (Oracle se conserva por si hay rollback).
    repositorio = PostgresRepositorio()

    # R3: el cliente recibe SMS y notificación push en cada transferencia.
    notificador = NotificadorCompuesto([SmsGateway(), PushNotifier()])

    validador = ValidadorTransferencia()
    calculador_comision = CalculadorComision()
    comprobante = GeneradorComprobante()
    auditor = AuditorTransferencia()

    # R4: cada transacción exitosa se reporta al sistema antifraude.
    antifraude = AntifraudeService()

    servicio = TransaccionService(
        repositorio,
        notificador,
        validador,
        calculador_comision,
        comprobante,
        auditor,
        observadores=[antifraude],
    )

    print("===== Transferencia a otro banco =====")
    servicio.transferir(ana, luis, 150_000, TransferenciaOtroBanco())

    # R1: transferencia por llave (celular/cédula), sin comisión.
    print("\n===== Transferencia por llave (R1) =====")
    servicio.transferir(ana, luis, 50_000, TransferenciaLlave())

    # R2: cuenta infantil con límite de retiro diario de $200.000.
    print("\n===== Cuenta infantil (R2) =====")
    sofia = CuentaInfantil("INF-1", "Sofia", 1_000_000)
    servicio.transferir(sofia, luis, 120_000, TransferenciaLlave())
    print(f"Saldo cuenta infantil tras retirar $120.000: ${sofia.get_saldo()}")
    try:
        servicio.transferir(sofia, luis, 100_000, TransferenciaLlave())
    except RuntimeError as e:
        print(f"Segundo retiro rechazado: {e}")
        print(f"Saldo cuenta infantil sin cambios: ${sofia.get_saldo()}")

    print("\n===== Cobro de cuota de manejo =====")
    CobroCuotaManejo().cobrar_mensual([ana, luis, sofia])

    print("\n===== Extractos de productos =====")
    productos = [
        TarjetaCredito(3_000_000),
        CreditoVivienda(120_000_000)
    ]
    for p in productos:
        print(p.generar_extracto())


if __name__ == "__main__":
    main()
