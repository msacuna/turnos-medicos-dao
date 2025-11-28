from abc import ABC, abstractmethod

class SujetoTurno(ABC):
    suscriptores = list()
    @abstractmethod
    def agregar_suscriptor(self, suscriptor):
        pass
    
    @abstractmethod
    def eliminar_suscriptor(self, suscriptor):
        pass

    @abstractmethod
    def notificar(self, pacientes: list[list[str]]):
        pass