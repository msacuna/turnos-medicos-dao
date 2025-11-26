from ..base import BaseRepository
from ...domain.models import EnProceso
from sqlmodel import select
from typing import Optional

class EnProcesoRepository(BaseRepository[EnProceso]):
    def get_by_nombre(self, nombre: str) -> Optional[EnProceso]:
        statement = select(EnProceso).where(EnProceso.nombre == nombre)
        return self.session.exec(statement).first()