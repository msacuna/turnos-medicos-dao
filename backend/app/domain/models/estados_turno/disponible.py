from estado_turno_abs import EstadoTurnoAbs
from app.domain.models.turno import Turno
from agendado import Agendado
from cancelado import Cancelado
from sqlmodel import SQLModel, Field
from typing import Optional

class Disponible(EstadoTurnoAbs, SQLModel, table=True):
    __tablename__ = "disponible"
    id: Optional[int] = Field(primary_key=True, default=None)
    nombre: str = Field(default="Disponible")

    def es_disponible(self) -> bool:
        return True
    
    def agendar(self, ctx: Turno, dni_paciente: str):
        # Lógica de negocio: agendar el turno
        ctx.dni_paciente = dni_paciente
        ctx.estado = Agendado() # Cambia el estado del turno a Agendado

    def cancelar(self, ctx: Turno):
        ctx.estado = Cancelado()