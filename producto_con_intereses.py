from abc import ABC, abstractmethod


class ProductoConIntereses(ABC):
    @abstractmethod
    def calcular_intereses(self) -> float:
        pass