class ValidadorTransferencia:
    TOPE_DIARIO = 5_000_000

    def validar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto inválido")

        if monto > self.TOPE_DIARIO:
            raise ValueError("Supera el tope diario")