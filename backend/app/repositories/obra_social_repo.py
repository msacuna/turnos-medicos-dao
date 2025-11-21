from typing import Optional
from sqlmodel import select
from app.domain.models import ObraSocial
from .base import BaseRepository

# Hereda de BaseRepository
class ObraSocialRepository(BaseRepository[ObraSocial]):
    
    def get_by_nombre(self, nombre: str) -> Optional[ObraSocial]:
        statement = select(ObraSocial).where(ObraSocial.nombre == nombre)
        return self.session.exec(statement).first()