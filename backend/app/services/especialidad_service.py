from app.domain.models import Especialidad
from app.domain.schemas import EspecialidadCreate, EspecialidadUpdate, EspecialidadRead
from app.repositories import EspecialidadRepository

class EspecialidadService:
    def __init__(self, repo: EspecialidadRepository):
        self.repo = repo

    def obtener_todas(self) -> list[EspecialidadRead]:
        especialidades = self.repo.get_all()
        return [EspecialidadRead.model_validate(e) for e in especialidades]
    
    def obtener_por_id(self, id: int) -> EspecialidadRead | None:
        especialidad = self.repo.get_by_id(id)
        if not especialidad:
            raise ValueError(f"No se encontró la especialidad con ID {id}.")
        return EspecialidadRead.model_validate(especialidad)

    def crear_especialidad(self, nombre: str) -> EspecialidadCreate:
        existente = self.repo.get_by_nombre(nombre)
        if existente:
            raise ValueError(f"La especialidad con nombre '{nombre}' ya existe.")
        nueva = Especialidad(nombre=nombre)
        return EspecialidadCreate.model_validate(self.repo.add(nueva))

    def actualizar(self, id: int, data: EspecialidadUpdate) -> Especialidad | None:
        especialidad_actual = self.repo.get_by_id(id)
        if not especialidad_actual:
            return None
        
        datos_limpios = data.model_dump(exclude_unset=True)
        return self.repo.update(especialidad_actual, datos_limpios)