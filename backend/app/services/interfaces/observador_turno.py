from abc import ABC, abstractmethod

class ObservadorTurno(ABC):
    mensaje: str = ""
    @abstractmethod
    def actualizar(self, pacientes: list[list[str]]):
        pass