from typing import List
from notificador import Notificador


class NotificadorCompuesto(Notificador):
    """R3 - Notificador compuesto (patrón Composite).

    Agrupa varios notificadores y los trata como uno solo. Gracias a esto
    TransaccionService sigue recibiendo un único Notificador y no cambia:
    basta con inyectarle este compuesto con la lista [SMS, Push].
    """

    def __init__(self, notificadores: List[Notificador]):
        self._notificadores = notificadores

    def enviar(self, destinatario: str, mensaje: str) -> None:
        for notificador in self._notificadores:
            notificador.enviar(destinatario, mensaje)
