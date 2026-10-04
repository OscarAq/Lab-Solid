from abc import ABC, abstractmethod


class ProductoBancario(ABC):
    @abstractmethod
    def generar_extracto(self) -> str:
        pass