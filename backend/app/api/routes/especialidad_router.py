from fastapi import APIRouter, Depends, status
from app.core import get_especialidad_service
from app.services import EspecialidadService
from app.models import Especialidad

router = APIRouter(prefix="/especialidades", tags=["Especialidades"])

# SIEMPRE VA SER NECESARIO INYECTAR EL SERVICIO EN CADA ENDPOINT POR LA SESSION
# osea es necesario pasar el db: Session por todas las capas (sino tira error 500)
# esto es uno de los problemitas de usar arquitectura de capas con FastAPI
@router.post("/", response_model=Especialidad, status_code=status.HTTP_201_CREATED)
def crear_especialidad(especialidad_in: Especialidad, service: EspecialidadService = Depends(get_especialidad_service)):
    return service.crear_especialidad(nombre=especialidad_in.nombre)

@router.get("/", response_model=list[Especialidad])
def listar_especialidades(service: EspecialidadService = Depends(get_especialidad_service)):
    return service.obtener_todas()

@router.get("/{id}", response_model=Especialidad)
def obtener_especialidad(id: int, service: EspecialidadService = Depends(get_especialidad_service)):
    return service.obtener_por_id(id)