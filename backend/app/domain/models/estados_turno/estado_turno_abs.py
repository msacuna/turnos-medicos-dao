from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.domain.models.turno import Turno

class EstadoTurnoAbs(ABC):

    nombre: str = ""

    def __init__(self):
        pass

    def cancelar(self, ctx: "Turno") -> None:
        raise NotImplementedError(f"Cancelar no disponible en estado {self.nombre}")
    
    def liberar(self, ctx: "Turno") -> None:
        raise NotImplementedError(f"Liberar no disponible en estado {self.nombre}")
    
    def agendar(self, ctx: "Turno", dni_paciente: int, cobertura: float) -> None:
        raise NotImplementedError(f"Agendar no disponible en estado {self.nombre}")
    
    def iniciarTurno(self, ctx: "Turno") -> None:
        raise NotImplementedError(f"Iniciar turno no disponible en estado {self.nombre}")
    
    def finalizarTurno(self, ctx: "Turno") -> None:
        raise NotImplementedError(f"Finalizar turno no disponible en estado {self.nombre}")
    
    def marcarInasistencia(self, ctx: "Turno") -> None:
        raise NotImplementedError(f"Marcar inasistencia no disponible en estado {self.nombre}")


    @abstractmethod
    def es_cancelado(self) -> bool:
        pass
    @abstractmethod
    def es_disponible(self) -> bool:
        pass
    @abstractmethod
    def es_agendado(self) -> bool:
        pass
    @abstractmethod
    def es_en_proceso(self) -> bool:
        pass
    @abstractmethod
    def es_finalizado(self) -> bool:
        pass
    @abstractmethod
    def es_ausente(self) -> bool:
        pass
    
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

    def agendar(self, ctx: "Turno", dni_paciente: int, cobertura: float) -> None:
        try:
            # Validaciones
            if not (0 <= cobertura <= 100):
                raise ValueError("La cobertura debe estar entre 0 y 100%")
        
            if not ctx.especialidad:
                raise ValueError("El turno debe tener una especialidad asignada")
            
            if not hasattr(ctx.especialidad, 'precio') or ctx.especialidad.precio <= 0:
                raise ValueError("La especialidad debe tener un precio válido")
            
            # Lógica de negocio: agendar el turno
            ctx.dni_paciente = dni_paciente
            ctx.monto = (1-(cobertura/100)) * ctx.especialidad.precio
            ctx.set_estado(Agendado()) # Cambia el estado del turno a Agendado
        
        except Exception as e:
            raise ValueError(f"Error al agendar turno: {str(e)}")

    def cancelar(self, ctx: "Turno") -> None:
        ctx.set_estado(Cancelado())
    
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
    def finalizarTurno(self, ctx: "Turno") -> None:
        ctx.set_estado(Finalizado())

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