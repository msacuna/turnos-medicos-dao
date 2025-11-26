from ..base import BaseRepository
from ...domain.models import Ausente
from sqlmodel import select
from typing import Optional

class AusenteRepository(BaseRepository[Ausente]):
    def get_by_nombre(self, nombre: str) -> Optional[Ausente]:
        statement = select(Ausente).where(Ausente.nombre == nombre)
        return self.session.exec(statement).first()