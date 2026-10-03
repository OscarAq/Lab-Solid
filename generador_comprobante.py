class GeneradorComprobante:
    def generar(self, origen, destino, monto: float, comision: float) -> None:
        print("===== BANCO ANDINO - COMPROBANTE =====")
        print(f"Origen: {origen.get_numero()}")
        print(f"Destino: {destino.get_numero()}")
        print(f"Monto: ${monto}")
        print(f"Comisión: ${comision}")
        print("=====================================")