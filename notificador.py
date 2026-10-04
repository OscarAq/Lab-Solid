from abc import ABC, abstractmethod


class Notificador(ABC):

    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str) -> None:
        pass