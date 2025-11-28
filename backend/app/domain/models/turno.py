from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import model_validator
from datetime import date, time
from .estados_turno.estado_turno_abs import EstadoTurnoAbs
from .estados_turno.registry import build_estado_turno

if TYPE_CHECKING:
    from .paciente import Paciente
    from .especialidad import Especialidad
    from .agenda_profesional import AgendaProfesional
    from .consulta import Consulta
    from .estados_turno.estado_turno_abs import EstadoTurnoAbs

class Turno(SQLModel, table=True):
    __tablename__ = "turno"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    hora_inicio: time
    hora_fin_estimada: time
    dni_paciente: Optional[int] = Field(foreign_key="paciente.dni", nullable=True)
    id_especialidad: int = Field(foreign_key="especialidad.id")
    id_agenda_profesional: int = Field(foreign_key="agenda_profesional.id")
    monto: float = Field(default=0.0)

    # Relación con el estado (State Pattern)  
    nombre_estado: str = Field(
        foreign_key="estados_turno.nombre",
        default="Disponible")

    paciente: Optional["Paciente"] = Relationship(back_populates="turnos")
    especialidad: Optional["Especialidad"] = Relationship(back_populates="turnos")
    agenda_profesional: Optional["AgendaProfesional"] = Relationship(back_populates="turnos")
    consultas: list["Consulta"] = Relationship(back_populates="turno")

    @model_validator(mode="after")
    def validar_rango_horario(self):
        if self.hora_fin_estimada <= self.hora_inicio:
            raise ValueError("hora_fin_estimada debe ser mayor que hora_inicio")
        return self

    def set_estado(self, nuevo_estado: "EstadoTurnoAbs") -> None:
        self.nombre_estado = nuevo_estado.nombre

    @property
    def estado(self) -> "EstadoTurnoAbs":
        return build_estado_turno(self.nombre_estado)
    
    def agendar(self, dni_paciente: int, cobertura: float) -> None:
        self.estado.agendar(self, dni_paciente, cobertura)
    
    def cancelar(self) -> None:
        self.estado.cancelar(self)
    
    def liberar(self) -> None:
        self.estado.liberar(self)
    
    def iniciar(self) -> None:
        self.estado.iniciarTurno(self)
    
    def finalizar(self) -> None:
        self.estado.finalizarTurno(self)
    
    def marcar_ausente(self) -> None:
        self.estado.marcarInasistencia(self)
    
    def es_disponible(self) -> bool:
        return self.estado.es_disponible()
    def es_agendado(self) -> bool:
        return self.estado.es_agendado()
    def es_en_proceso(self) -> bool:
        return self.estado.es_en_proceso()
    def es_finalizado(self) -> bool:
        return self.estado.es_finalizado()
    def es_cancelado(self) -> bool:
        return self.estado.es_cancelado()
    def es_ausente(self) -> bool:
        return self.estado.es_ausente()
    def get_nombre_estado(self) -> str:
        return self.estado.get_name()
    