from ..base import BaseRepository
from ...domain.models import Cancelado
from sqlalchemy.future import select
from typing import Optional

class CanceladoRepository(BaseRepository[Cancelado]):
    def get_by_nombre(self, nombre: str) -> Optional[Cancelado]:
        statement = select(Cancelado).where(Cancelado.nombre == nombre)
        return self.session.exec(statement).first()