from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_medicamento_service
from app.services import MedicamentoService
from app.domain.schemas import MedicamentoCreate, MedicamentoUpdate, MedicamentoRead

router = APIRouter(prefix="/medicamentos", tags=["Medicamentos"])

@router.post("/", response_model=MedicamentoRead, status_code=status.HTTP_201_CREATED)
def crear_medicamento(medicamento_in: MedicamentoCreate, service: MedicamentoService = Depends(get_medicamento_service)):
    return service.crear_medicamento(medicamento_in)

@router.get("/", response_model=list[MedicamentoRead])
def listar_medicamentos(service: MedicamentoService = Depends(get_medicamento_service)):
    return service.obtener_todos()

@router.get("/{id}", response_model=MedicamentoRead)
def obtener_medicamento(id: int, service: MedicamentoService = Depends(get_medicamento_service)):
    return service.obtener_por_id(id)

@router.put("/{id}", response_model=MedicamentoRead)
def actualizar_medicamento(id: int, medicamento_in: MedicamentoUpdate, service: MedicamentoService = Depends(get_medicamento_service)):
    return service.actualizar(id, medicamento_in)