from fastapi import APIRouter, Depends, status
from app.api.dependencies import get_paciente_service
from app.services import PacienteService
from app.domain.schemas import PacienteCreate, PacienteRead, PacienteUpdate

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@router.post("/", response_model=PacienteRead, status_code=status.HTTP_201_CREATED)
def crear_paciente(paciente_in: PacienteCreate, service: PacienteService = Depends(get_paciente_service)):
    return service.crear_paciente(paciente_in)

@router.get("/", response_model=list[PacienteRead])
def listar_pacientes(service: PacienteService = Depends(get_paciente_service)):
    return service.obtener_todos()

@router.get("/{dni}", response_model=PacienteRead)
def obtener_paciente(dni: int, service: PacienteService = Depends(get_paciente_service)):
    return service.obtener_por_id(dni)

@router.put("/{dni}", response_model=PacienteRead)
def actualizar_paciente(dni: int, paciente_in: PacienteUpdate, service: PacienteService = Depends(get_paciente_service)):
    return service.actualizar(dni, paciente_in)