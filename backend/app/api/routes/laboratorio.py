from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_laboratorio_service
from app.services import LaboratorioService
from app.domain.schemas import LaboratorioCreate, LaboratorioUpdate, LaboratorioRead

router = APIRouter(prefix="/laboratorios", tags=["Laboratorios"])

@router.post("/", response_model=LaboratorioRead, status_code=status.HTTP_201_CREATED)
def crear_laboratorio(laboratorio_in: LaboratorioCreate, service: LaboratorioService = Depends(get_laboratorio_service)):
    return service.crear_laboratorio(laboratorio_in)

@router.get("/", response_model=list[LaboratorioRead])
def listar_laboratorios(service: LaboratorioService = Depends(get_laboratorio_service)):
    return service.obtener_todos()

@router.get("/{id}", response_model=LaboratorioRead)
def obtener_laboratorio(id: int, service: LaboratorioService = Depends(get_laboratorio_service)):
    return service.obtener_por_id(id)

@router.put("/{id}", response_model=LaboratorioRead)
def actualizar_laboratorio(id: int, laboratorio_in: LaboratorioUpdate, service: LaboratorioService = Depends(get_laboratorio_service)):
    return service.actualizar(id, laboratorio_in)