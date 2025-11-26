from typing import Optional
from sqlmodel import select
from app.domain.models import Profesional
from app.domain.schemas.profesional import ProfesionalCreate, ProfesionalRead
from .base import BaseRepository

class ProfesionalRepository(BaseRepository[Profesional]):
    
    def get_by_nombre(self, nombre: str) -> Optional[Profesional]:
        statement = select(Profesional).where(Profesional.nombre == nombre)
        return self.session.exec(statement).first()
    
    def get_by_especialidad(self, especialidad: str) -> list[Profesional]:
        statement = select(Profesional).where(Profesional.especialidad == especialidad)
        return list(self.session.exec(statement).all())
    
    def crear_profesional(self, profesional_data: ProfesionalCreate) -> ProfesionalRead:
        # 1. Validar que la especialidad existe (si aplica)
        if hasattr(profesional_data, 'nombre_especialidad'):
            if not self.especialidad_service.existe_especialidad(profesional_data.nombre_especialidad):
                raise ValueError(f"No se encontró la especialidad {profesional_data.nombre_especialidad}")
        
        # 2. Convertir schema a modelo
        datos_profesional = profesional_data.model_dump()
        nuevo_profesional = Profesional.model_validate(datos_profesional)
        
        # 3. Crear en base de datos
        profesional_creado = self.profesional_repo.create(nuevo_profesional)
        
        # 4. Retornar schema de lectura
        return ProfesionalRead.model_validate(profesional_creado)