from abc import ABC, abstractmethod

from sqlmodel import Field

class EstadoTurnoAbs(ABC):

    id: int = Field(primary_key=True)
    nombre: str = Field()

    def __init__(self):
        pass

    @abstractmethod
    def cancelar(self, ctx) -> None:
        raise NotImplementedError("Cancelar no implementado para este estado")
    @abstractmethod
    def liberar(self, ctx) -> None:
        raise NotImplementedError("Liberar no implementado para este estado")
    @abstractmethod
    def agendar(self, ctx) -> None:
        raise NotImplementedError("Agendar no implementado para este estado")
    @abstractmethod
    def iniciarTurno(self, ctx) -> None:
        raise NotImplementedError("IniciarTurno no implementado para este estado")
    @abstractmethod
    def finalizarTurno(self, ctx) -> None:
        raise NotImplementedError("FinalizarTurno no implementado para este estado")
    @abstractmethod
    def marcarInasistencia(self, ctx) -> None:
        raise NotImplementedError("MarcarInasistencia no implementado para este estado")

    @abstractmethod
    def es_cancelado(self) -> bool:
        return False
    @abstractmethod
    def es_disponible(self) -> bool:
        return False
    @abstractmethod
    def es_agendado(self) -> bool:
        return False
    @abstractmethod
    def es_en_proceso(self) -> bool:
        return False
    @abstractmethod
    def es_finalizado(self) -> bool:
        return False
    @abstractmethod
    def es_ausente(self) -> bool:
        return False
    
