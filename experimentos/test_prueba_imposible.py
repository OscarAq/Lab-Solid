"""
Bloque 1 - Experimento 2: La prueba imposible.

Intenta verificar que una transferencia a otro banco cobra $7.500 de
comisión SIN conectarse a Oracle ni enviar SMS.

El assert sobre la comisión pasa, pero la prueba NO puede evitar que se
ejecuten el repositorio y el SMS, porque TransaccionService crea sus
dependencias dentro de __init__ (no hay inyección). Esto es la violación
del Principio de Inversión de Dependencias (DIP).

Correr con salida visible para ver los [ORACLE] y [SMS] que se disparan:
    pytest experimentos/test_prueba_imposible.py -s
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuenta_ahorros import CuentaAhorros
from transaccion_service import TransaccionService


def test_comision_otro_banco_cobra_7500():
    origen = CuentaAhorros("001-1", "Ana", 2_000_000)
    destino = CuentaAhorros("001-2", "Luis", 500_000)
    # Al construir el servicio ya se instancian OracleRepositorio y SmsGateway:
    # no hay forma de inyectar dobles de prueba.
    servicio = TransaccionService()
    servicio.transferir(origen, destino, 100_000, "OTRO_BANCO")
    # El saldo sí es verificable; lo que NO se puede evitar es el golpe a
    # Oracle ni el envío del SMS (visibles en la consola con pytest -s).
    assert origen.get_saldo() == 2_000_000 - 100_000 - 7_500
