


from fastapi import APIRouter, Depends, HTTPException
from app.domain.schemas.turno import TurnoRead, TurnoCreate, TurnoUpdate
from app.api.dependencies import get_turno_service
from app.domain.schemas.consulta import ConsultaCreate
from app.services.turno_service import TurnoService

router = APIRouter(prefix="/turnos", tags=["Turnos"])

@router.patch("/{turno_id}/agendar/{dni_paciente}", response_model=TurnoRead)
def agendar_turno(
    turno_id: int,
    dni_paciente: int,
    service: TurnoService = Depends(get_turno_service)
):
    try:
        return service.agendar_turno(turno_id, dni_paciente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/{turno_id}/liberar", response_model=TurnoRead)
def liberar_turno(
    turno_id: int,
    service: TurnoService = Depends(get_turno_service)
):
    try:
        return service.liberar_turno(turno_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/{turno_id}/iniciar", response_model=TurnoRead)
def iniciar_turno(
    turno_id: int,
    service: TurnoService = Depends(get_turno_service)
):
    try:
        return service.iniciar_turno(turno_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.patch("/{turno_id}/finalizar", response_model=TurnoRead)
def finalizar_turno(
    turno_id: int,
    consulta_data: ConsultaCreate,
    service: TurnoService = Depends(get_turno_service)
):
    try:
        return service.finalizar_turno(turno_id, consulta_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
