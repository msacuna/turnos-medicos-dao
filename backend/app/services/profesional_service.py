
from app.repositories.profesional_repo import ProfesionalRepository
from app.services.especialidad_service import EspecialidadService
from app.domain.schemas.profesional import ProfesionalCreate, ProfesionalRead
from app.domain.models import Profesional
from app.services.agenda_profesional_service import AgendaProfesionalService


class ProfesionalService:
    def __init__(self, profesional_repo: ProfesionalRepository, especialidad_service: EspecialidadService):
        self.profesional_repo = profesional_repo
        self.especialidad_service = especialidad_service


    def crear_profesional(self, profesional_data: ProfesionalCreate) -> ProfesionalRead:
        # 1. Validar que la especialidad existe usando el id_especialidad
        if not self.especialidad_service.existe_especialidad_por_id(profesional_data.id_especialidad):
            raise ValueError(f"No se encontró la especialidad con ID {profesional_data.id_especialidad}")
        
        # 2. Convertir schema a modelo
        datos_profesional = profesional_data.model_dump()
        nuevo_profesional = Profesional.model_validate(datos_profesional)
        
        # 3. Crear en base de datos
        profesional_creado = self.profesional_repo.create(nuevo_profesional)
        
        # 4. Retornar schema de lectura
        return ProfesionalRead.model_validate(profesional_creado)
    
    def crear_agenda(self, id_profesional: int):
        profesional = self.profesional_repo.get_by_id(id_profesional)
        if not profesional:
            raise ValueError(f"No se encontró el profesional con ID {id_profesional}")
        

        
        