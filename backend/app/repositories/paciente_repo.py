from typing import Optional
from sqlmodel import select
from app.domain.models import Paciente
from .base import BaseRepository

class PacienteRepository(BaseRepository[Paciente]):

    def get_by_dni(self, dni: int) -> Optional[Paciente]:
        statement = select(Paciente).where(Paciente.dni == dni)
        return self.session.exec(statement).first()
    
    def get_by_email(self, email: str) -> Optional[Paciente]:
        statement = select(Paciente).where(Paciente.email == email)
        return self.session.exec(statement).first()
    
    def get_all_by_apellido(self, apellido: str) -> list[Paciente]:
        statement = select(Paciente).where(Paciente.apellido == apellido)
        return list(self.session.exec(statement).all())