from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_antecedente_service
from app.services import AntecedenteService
from app.domain.schemas import AntecedenteCreate, AntecedenteUpdate, AntecedenteRead

router = APIRouter(prefix="/antecedentes", tags=["Antecedentes"])

@router.post("/", response_model=AntecedenteRead, status_code=status.HTTP_201_CREATED)
def crear_antecedente(antecedente_in: AntecedenteCreate, service: AntecedenteService = Depends(get_antecedente_service)):
    return service.crear_antecedente(antecedente_in)

@router.get("/", response_model=list[AntecedenteRead])
def listar_antecedentes(service: AntecedenteService = Depends(get_antecedente_service)):
    return service.obtener_todos()

@router.get("/{id}", response_model=AntecedenteRead)
def obtener_antecedente(id: int, service: AntecedenteService = Depends(get_antecedente_service)):
    return service.obtener_por_id(id)

@router.put("/{id}", response_model=AntecedenteRead)
def actualizar_antecedente(id: int, antecedente_in: AntecedenteUpdate, service: AntecedenteService = Depends(get_antecedente_service)):
    return service.actualizar(id, antecedente_in)