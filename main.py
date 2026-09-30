from datetime import date
from cuenta_ahorros import CuentaAhorros
from cdt import CDT
from transaccion_service import TransaccionService
from cobro_cuota_manejo import CobroCuotaManejo
from tarjeta_credito import TarjetaCredito
from credito_vivienda import CreditoVivienda

def main():
    ana = CuentaAhorros("001-1", "Ana", 2_000_000)
    luis = CuentaAhorros("001-2", "Luis", 500_000)
    
    # Se agrega 6 meses al CDT (aproximado)
    cdt_ana = CDT("CDT-9", "Ana", 10_000_000, date(2026, 9, 30))

    servicio = TransaccionService()
    servicio.transferir(ana, luis, 150_000, "OTRO_BANCO")

    CobroCuotaManejo().cobrar_mensual([ana, luis])

    productos = [
        TarjetaCredito(3_000_000),
        CreditoVivienda(120_000_000)
    ]
    for p in productos:
        print(p.generar_extracto())

if __name__ == "__main__":
    main()