from cuenta_ahorros import CuentaAhorros
from transaccion_service import TransaccionService
from validador_transferencia import ValidadorTransferencia
from calculador_comision import CalculadorComision
from generador_comprobante import GeneradorComprobante
from auditor_transferencia import AuditorTransferencia
from transferencia_mismo_banco import TransferenciaMismoBanco
from transferencia_otro_banco import TransferenciaOtroBanco
from tipo_transferencia import TipoTransferencia
import pytest

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


def crear_servicio():
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

    return servicio, repositorio, notificador


#Prueba 1
def test_transferencia_mismo_banco_no_cobra_comision():
    origen = CuentaAhorros("001-1", "Ana", 2_000_000)
    destino = CuentaAhorros("001-2", "Luis", 500_000)

    servicio, repositorio, notificador = crear_servicio()

    servicio.transferir(
        origen,
        destino,
        150_000,
        TransferenciaMismoBanco()
    )

    assert origen.get_saldo() == 1_850_000
    assert destino.get_saldo() == 650_000
    assert repositorio.transacciones[0]["comision"] == 0

#Prueba 2
def test_transferencia_otro_banco_cobra_comision():
    origen = CuentaAhorros("001-1", "Ana", 2_000_000)
    destino = CuentaAhorros("001-2", "Luis", 500_000)

    servicio, repositorio, notificador = crear_servicio()

    from transferencia_otro_banco import TransferenciaOtroBanco

    servicio.transferir(
        origen,
        destino,
        150_000,
        TransferenciaOtroBanco()
    )

    assert origen.get_saldo() == 1_842_500
    assert destino.get_saldo() == 650_000
    assert repositorio.transacciones[0]["comision"] == 7_500

#Prueba 3
def test_saldo_insuficiente_no_guarda_ni_notifica():
    origen = CuentaAhorros("001-1", "Ana", 100_000)
    destino = CuentaAhorros("001-2", "Luis", 500_000)

    servicio, repositorio, notificador = crear_servicio()

    with pytest.raises(RuntimeError, match="Saldo insuficiente"):
        servicio.transferir(
            origen,
            destino,
            150_000,
            TransferenciaOtroBanco()
        )

    assert origen.get_saldo() == 100_000
    assert destino.get_saldo() == 500_000
    assert len(repositorio.transacciones) == 0
    assert len(notificador.notificaciones) == 0

#Prueba 4
def test_transferencia_exitosa_guarda_y_notifica_una_vez():
    origen = CuentaAhorros("001-1", "Ana", 2_000_000)
    destino = CuentaAhorros("001-2", "Luis", 500_000)

    servicio, repositorio, notificador = crear_servicio()

    servicio.transferir(origen,destino,150_000,TransferenciaMismoBanco())

    assert len(repositorio.transacciones) == 1
    assert len(notificador.notificaciones) == 1


#Prueba 5
class TransferenciaDesconocida(TipoTransferencia):

    def calcular_comision(self, monto: float) -> float:
        raise ValueError("Tipo de transferencia desconocido")

    def nombre(self) -> str:
        return "DESCONOCIDO"


def test_tipo_transferencia_desconocido_rechaza_y_no_cambia_saldo():
    origen = CuentaAhorros("001-1", "Ana", 2_000_000)
    destino = CuentaAhorros("001-2", "Luis", 500_000)

    servicio, repositorio, notificador = crear_servicio()

    with pytest.raises(ValueError, match="Tipo de transferencia desconocido"):
        servicio.transferir(
            origen,
            destino,
            150_000,
            TransferenciaDesconocida()
        )

    assert origen.get_saldo() == 2_000_000
    assert destino.get_saldo() == 500_000
    assert len(repositorio.transacciones) == 0
    assert len(notificador.notificaciones) == 0