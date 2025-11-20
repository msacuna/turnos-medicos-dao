from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_especialidad_service
from app.services import EspecialidadService
from app.domain.models import Especialidad
from app.domain.schemas import EspecialidadCreate, EspecialidadUpdate, EspecialidadRead

router = APIRouter(prefix="/especialidades", tags=["Especialidades"])

# SIEMPRE VA SER NECESARIO INYECTAR EL SERVICIO EN CADA ENDPOINT POR LA SESSION
# osea es necesario pasar el db: Session por todas las capas (sino tira error 500)
# esto es uno de los problemitas de usar arquitectura de capas con FastAPI
@router.post("/", response_model=EspecialidadCreate, status_code=status.HTTP_201_CREATED)
def crear_especialidad(especialidad_in: EspecialidadCreate, service: EspecialidadService = Depends(get_especialidad_service)):
    return service.crear_especialidad(nombre=especialidad_in.nombre)

@router.get("/", response_model=list[EspecialidadRead])
def listar_especialidades(service: EspecialidadService = Depends(get_especialidad_service)):
    return service.obtener_todas()

@router.get("/{id}", response_model=EspecialidadRead)
def obtener_especialidad(id: int, service: EspecialidadService = Depends(get_especialidad_service)):
    return service.obtener_por_id(id)

@router.put("/{id}", response_model=EspecialidadRead)
def actualizar_especialidad(id: int, especialidad_in: EspecialidadUpdate, service: EspecialidadService = Depends(get_especialidad_service)):
    return service.actualizar(id, especialidad_in)