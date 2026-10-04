from notificador import Notificador


class SmsGateway(Notificador):

    def enviar(self, destinatario: str, mensaje: str) -> None:
        print("[SMS] Conectando al proveedor de mensajeria...")
        print(f"[SMS] Para {destinatario}: {mensaje}")