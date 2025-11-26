from sqlmodel import select
from typing import Optional
from ..base import BaseRepository
from ...domain.models import Agendado

class AgendadoRepository(BaseRepository[Agendado]):
    def get_by_nombre(self, nombre: str) -> Optional[Agendado]:
        statement = select(Agendado).where(Agendado.nombre == nombre)
        return self.session.exec(statement).first()