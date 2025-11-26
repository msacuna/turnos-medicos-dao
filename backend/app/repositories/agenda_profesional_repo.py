

from backend.app.domain.models.agenda_profesional import AgendaProfesional
from backend.app.repositories.base import BaseRepository
from sqlmodel import select
from typing import Optional


class AgendaProfesionalRepo(BaseRepository[AgendaProfesional]):
    def get_agenda_by_profesional_id(self, profesional_id: int) -> AgendaProfesional | None:
        statement = (
            self.select_statement()
            .where(AgendaProfesional.profesional_id == profesional_id)
        )
        result = self.session.exec(statement).first()
        return result
    
    def get_agenda_by_profesional_anio_mes(self, id_profesional: int, anio: int, mes: int) -> Optional[AgendaProfesional]:
        """Verifica si ya existe una agenda para un profesional en un año y mes específico"""
        statement = select(AgendaProfesional).where(
            AgendaProfesional.id_profesional == id_profesional,
            AgendaProfesional.anio == anio,
            AgendaProfesional.mes == mes
        )
        return self.session.exec(statement).first()