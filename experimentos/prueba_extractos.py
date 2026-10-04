import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from cuenta_ahorros import CuentaAhorros
from tarjeta_credito import TarjetaCredito
from credito_vivienda import CreditoVivienda
from generador_extractos import GeneradorExtractos


def main():
    cuenta = CuentaAhorros("001-1", "Ana", 2_000_000)
    tarjeta = TarjetaCredito(3_000_000)
    credito = CreditoVivienda(120_000_000)

    generador = GeneradorExtractos()

    print(generador.generar(cuenta))
    print(generador.generar(tarjeta))
    print(generador.generar(credito))


if __name__ == "__main__":
    main()