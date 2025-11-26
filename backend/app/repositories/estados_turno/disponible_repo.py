from ..base import BaseRepository
from ...domain.models import Disponible
from sqlmodel import select
from typing import Optional

class DisponibleRepository(BaseRepository[Disponible]):
    def get_by_nombre(self, nombre: str) -> Optional[Disponible]:
        statement = select(Disponible).where(Disponible.nombre == nombre)
        return self.session.exec(statement).first()