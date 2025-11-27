from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.domain.models.turno import Turno

class EstadoTurnoAbs(ABC):

    nombre: str = ""

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
    
    def get_name(self) -> str:
        return self.nombre
    

class Ausente(EstadoTurnoAbs):
    nombre: str = "Ausente"

    def es_ausente(self) -> bool:
        return True
    
    def es_cancelado(self) -> bool:
        return False
    def es_disponible(self) -> bool:
        return False
    def es_agendado(self) -> bool:
        return False
    def es_en_proceso(self) -> bool:
        return False
    def es_finalizado(self) -> bool:
        return False
    def cancelar(self, ctx) -> None:
        super().cancelar(ctx)
    def liberar(self, ctx) -> None:
        super().liberar(ctx)
    def agendar(self, ctx) -> None:
        super().agendar(ctx)
    def iniciarTurno(self, ctx) -> None:
        super().iniciarTurno(ctx)
    def finalizarTurno(self, ctx) -> None:
        super().finalizarTurno(ctx)
    def marcarInasistencia(self, ctx) -> None:
        super().marcarInasistencia(ctx)

class Cancelado(EstadoTurnoAbs):
    nombre: str = "Cancelado"

    def es_cancelado(self) -> bool:
        return True
    
    def es_ausente(self) -> bool:
        return False
    def es_disponible(self) -> bool:
        return False
    def es_agendado(self) -> bool:
        return False
    def es_en_proceso(self) -> bool:
        return False
    def es_finalizado(self) -> bool:
        return False
    def cancelar(self, ctx) -> None:
        super().cancelar(ctx)
    def liberar(self, ctx) -> None:
        super().liberar(ctx)
    def agendar(self, ctx) -> None:
        super().agendar(ctx)
    def iniciarTurno(self, ctx) -> None:
        super().iniciarTurno(ctx)
    def finalizarTurno(self, ctx) -> None:
        super().finalizarTurno(ctx)
    def marcarInasistencia(self, ctx) -> None:
        super().marcarInasistencia(ctx)

class Disponible(EstadoTurnoAbs):
    nombre: str = "Disponible"

    def es_disponible(self) -> bool:
        return True
    
    def es_ausente(self) -> bool:
        return False
    def es_cancelado(self) -> bool:
        return False
    def es_agendado(self) -> bool:
        return False
    def es_en_proceso(self) -> bool:
        return False
    def es_finalizado(self) -> bool:
        return False
    
    def agendar(self, ctx: "Turno", dni_paciente: int, cobertura: float):
        # Lógica de negocio: agendar el turno
        ctx.dni_paciente = dni_paciente
        ctx.monto = (1-(cobertura/100)) * ctx.especialidad.precio
        ctx.set_estado(Agendado()) # Cambia el estado del turno a Agendado

    def cancelar(self, ctx: "Turno"):
        ctx.set_estado(Cancelado())
    
    def liberar(self, ctx) -> None:
        super().liberar(ctx)
    def iniciarTurno(self, ctx) -> None:
        super().iniciarTurno(ctx)
    def finalizarTurno(self, ctx) -> None:
        super().finalizarTurno(ctx)
    def marcarInasistencia(self, ctx) -> None:
        super().marcarInasistencia(ctx)

class EnProceso(EstadoTurnoAbs):
    nombre: str = "En Proceso"

    def es_en_proceso(self) -> bool:
        return True
    
    def es_ausente(self) -> bool:
        return False
    def es_cancelado(self) -> bool:
        return False
    def es_agendado(self) -> bool:
        return False
    def es_disponible(self) -> bool:
        return False
    def es_finalizado(self) -> bool:
        return False
    def cancelar(self, ctx) -> None:
        super().cancelar(ctx)
    def liberar(self, ctx) -> None:
        super().liberar(ctx)
    def agendar(self, ctx) -> None:
        super().agendar(ctx)
    def iniciarTurno(self, ctx) -> None:
        super().iniciarTurno(ctx)
    def finalizarTurno(self, ctx) -> None:
        ctx.set_estado(Finalizado())
    def marcarInasistencia(self, ctx) -> None:
        super().marcarInasistencia(ctx)

class Finalizado(EstadoTurnoAbs):
    nombre: str = "Finalizado"

    def es_finalizado(self) -> bool:
        return True
    
    def es_ausente(self) -> bool:
        return False
    def es_cancelado(self) -> bool:
        return False
    def es_agendado(self) -> bool:
        return False
    def es_en_proceso(self) -> bool:
        return False
    def es_disponible(self) -> bool:
        return False
    def cancelar(self, ctx) -> None:
        super().cancelar(ctx)
    def liberar(self, ctx) -> None:
        super().liberar(ctx)
    def agendar(self, ctx) -> None:
        super().agendar(ctx)
    def iniciarTurno(self, ctx) -> None:
        super().iniciarTurno(ctx)
    def finalizarTurno(self, ctx) -> None:
        super().finalizarTurno(ctx)
    def marcarInasistencia(self, ctx) -> None:
        super().marcarInasistencia(ctx)

class Agendado(EstadoTurnoAbs):
    nombre: str = "Agendado"

    def es_agendado(self) -> bool:
        return True
    
    def es_ausente(self) -> bool:
        return False
    def es_cancelado(self) -> bool:
        return False
    def es_disponible(self) -> bool:
        return False
    def es_en_proceso(self) -> bool:
        return False
    def es_finalizado(self) -> bool:
        return False
    
    def liberar(self, ctx: "Turno"):
        ctx.dni_paciente = None
        ctx.monto = 0.0
        ctx.set_estado(Disponible())

    def cancelar(self, ctx: "Turno"):
        ctx.set_estado(Cancelado())
    
    def marcarInasistencia(self, ctx: "Turno"):
        ctx.set_estado(Ausente())

    def iniciarTurno(self, ctx: "Turno"):
        ctx.set_estado(EnProceso())

    def agendar(self, ctx) -> None:
        super().agendar(ctx)
    def finalizarTurno(self, ctx) -> None:
        super().finalizarTurno(ctx)