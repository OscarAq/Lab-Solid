from observador_transaccion import ObservadorTransaccion


class AntifraudeService(ObservadorTransaccion):
    """R4 - Sistema antifraude del banco.

    Por regulación, cada transacción exitosa se reporta al sistema
    antifraude (simulado con un mensaje en consola). Se implementa como
    observador: TransaccionService lo invoca al final del flujo, solo
    cuando la transferencia fue exitosa. Una transferencia rechazada
    nunca llega a este punto, por lo que no genera reporte.
    """

    def registrar_transaccion(
        self,
        origen,
        destino,
        monto: float,
        comision: float,
        tipo: str,
    ) -> None:
        print(
            f"[ANTIFRAUDE] Analizando transaccion {tipo} "
            f"{origen.get_numero()}->{destino.get_numero()} "
            f"por ${monto} (comision ${comision})"
        )
