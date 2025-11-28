from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_alergia_service
from app.services import AlergiaService
from app.domain.schemas import AlergiaCreate, AlergiaUpdate, AlergiaRead

router = APIRouter(prefix="/alergias", tags=["Alergias"])

@router.post("/", response_model=AlergiaRead, status_code=status.HTTP_201_CREATED)
def crear_alergia(alergia_in: AlergiaCreate, service: AlergiaService = Depends(get_alergia_service)):
    return service.crear_alergia(alergia_in)

@router.get("/", response_model=list[AlergiaRead])
def listar_alergias(service: AlergiaService = Depends(get_alergia_service)):
    return service.obtener_todas()

@router.get("/{id}", response_model=AlergiaRead)
def obtener_alergia(id: int, service: AlergiaService = Depends(get_alergia_service)):
    return service.obtener_por_id(id)

@router.put("/{id}", response_model=AlergiaRead)
def actualizar_alergia(id: int, alergia_in: AlergiaUpdate, service: AlergiaService = Depends(get_alergia_service)):
    return service.actualizar(id, alergia_in)