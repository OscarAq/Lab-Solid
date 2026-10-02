"""
Bloque 1 - Experimento 1: El CDT.

Demuestra la violación del Principio de Sustitución de Liskov (LSP):
un CDT hereda de Cuenta pero rompe el contrato de retirar(), de modo que
el cobro masivo de cuota de manejo se detiene al llegar al CDT y las
cuentas posteriores nunca se cobran.

Ejecutar desde la raíz del repositorio:
    python experimentos/experimento1_cdt.py

Nota: se usa un CDT NO vencido (date.today() + 180 días), fiel al Java
original (LocalDate.now().plusMonths(6)). Con el CDT ya vencido el
experimento no fallaría.
"""
import os
import sys
from datetime import date, timedelta

# Permite importar los módulos de la raíz al correr desde experimentos/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cuenta_ahorros import CuentaAhorros
from cdt import CDT
from cobro_cuota_manejo import CobroCuotaManejo

ana = CuentaAhorros("001-1", "Ana", 2_000_000)
luis = CuentaAhorros("001-2", "Luis", 500_000)
cdt_ana = CDT("CDT-9", "Ana", 10_000_000, date.today() + timedelta(days=180))

print(">>> Lista a cobrar: [ana, cdt_ana, luis]")
CobroCuotaManejo().cobrar_mensual([ana, cdt_ana, luis])
print(">>> FIN (si ves esto, no falló)")
