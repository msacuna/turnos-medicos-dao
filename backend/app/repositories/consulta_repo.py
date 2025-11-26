import select
from typing import Optional

from app.domain.models.consulta import Consulta

from .base import BaseRepository

class ConsultaRepository(BaseRepository[Consulta]):
    
    def get_by_turno_id(self, turno_id: int) -> Optional[Consulta]:
        statement = select(Consulta).where(Consulta.turno_id == turno_id)
        return self.session.exec(statement).first()
    