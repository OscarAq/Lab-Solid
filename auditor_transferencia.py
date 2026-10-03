from datetime import datetime


class AuditorTransferencia:
    def registrar(self, tipo: str, origen, destino, monto: float) -> None:
        print(
            f"[AUDITORIA] {datetime.now()} "
            f"{tipo} {origen.get_numero()}->{destino.get_numero()} ${monto}"
        )