from typing import Optional
from sqlmodel import select
from app.domain.models import Alergia
from .base import BaseRepository

# Hereda de BaseRepository
class AlergiaRepository(BaseRepository[Alergia]):
    
    def get_by_nombre(self, nombre: str) -> Optional[Alergia]:
        statement = select(Alergia).where(Alergia.nombre == nombre)
        return self.session.exec(statement).first()