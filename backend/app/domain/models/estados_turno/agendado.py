from typing import Optional
from sqlmodel import SQLModel, Field
from estado_turno_abs import EstadoTurnoAbs
from app.domain.models.turno import Turno 
from disponible import Disponible
from cancelado import Cancelado
from en_proceso import EnProceso
from ausente import Ausente

class Agendado(EstadoTurnoAbs, SQLModel, table=True):
    __tablename__ = "agendado"
    id: Optional[int] = Field(primary_key=True, default=None)
    nombre: str = Field(default="Agendado")

    def es_agendado(self) -> bool:
        return True
    
    def liberar(self, ctx: Turno):
        ctx.dni_paciente = None
        ctx.estado = Disponible()

    def cancelar(self, ctx: Turno):
        ctx.estado = Cancelado()
    
    def marcar_inasistencia(self, ctx: Turno):
        ctx.estado = Ausente()

    def iniciarTurno(self, ctx: Turno):
        ctx.estado = EnProceso()