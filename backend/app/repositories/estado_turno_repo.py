from sqlmodel import select
from sqlalchemy import func
from app.repositories.base import BaseRepository
from app.domain.models.estados_turno.estado_turno import EstadoTurno


class EstadoTurnoRepository(BaseRepository[EstadoTurno]):
    def get_by_nombre(self, nombre: str) -> EstadoTurno | None:
        statement = select(EstadoTurno).where(
            func.lower(EstadoTurno.nombre) == func.lower(nombre)
        )
        result = self.session.exec(statement).first()
        return result