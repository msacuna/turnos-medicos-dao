from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_obra_social_service
from app.services import ObraSocialService
from app.domain.schemas import ObraSocialCreate, ObraSocialUpdate, ObraSocialRead

router = APIRouter(prefix="/obras-sociales", tags=["Obras Sociales"])

@router.post("/", response_model=ObraSocialRead, status_code=status.HTTP_201_CREATED)
def crear_obra_social(obra_social_in: ObraSocialCreate, service: ObraSocialService = Depends(get_obra_social_service)):
    return service.crear_obra_social(obra_social_in)

@router.get("/", response_model=list[ObraSocialRead])
def listar_obras_sociales(service: ObraSocialService = Depends(get_obra_social_service)):
    return service.obtener_todas()

@router.get("/{id}", response_model=ObraSocialRead)
def obtener_obra_social(id: int, service: ObraSocialService = Depends(get_obra_social_service)):
    return service.obtener_por_id(id)

@router.put("/{id}", response_model=ObraSocialRead)
def actualizar_obra_social(id: int, obra_social_in: ObraSocialUpdate, service: ObraSocialService = Depends(get_obra_social_service)):
    return service.actualizar(id, obra_social_in)