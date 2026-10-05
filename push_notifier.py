from notificador import Notificador


class PushNotifier(Notificador):
    """R3 - Notificación push en la app.

    Implementa la misma abstracción Notificador que SmsGateway, por lo que
    puede combinarse con el SMS sin que TransaccionService lo sepa.
    """

    def enviar(self, destinatario: str, mensaje: str) -> None:
        print("[PUSH] Enviando notificacion push a la app...")
        print(f"[PUSH] Para {destinatario}: {mensaje}")
