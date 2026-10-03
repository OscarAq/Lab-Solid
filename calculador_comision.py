class CalculadorComision:
    def calcular(self, monto: float, tipo: str) -> float:
        if tipo == "MISMO_BANCO":
            return 0.0

        if tipo == "OTRO_BANCO":
            return 7_500.0

        if tipo == "INTERNACIONAL":
            return (monto * 0.03) + 25_000.0

        raise ValueError("Tipo de transferencia desconocido")