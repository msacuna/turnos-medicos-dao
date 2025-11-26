# app/api/routes/profesionales.py
from fastapi import APIRouter, Depends, HTTPException, Body
from app.api.dependencies import get_agenda_profesional_service, get_horario_profesional_service, get_profesional_service
from app.services import HorarioProfesionalService, ProfesionalService
from app.domain.schemas import HorarioProfesionalRead, HorarioDiaInput, ProfesionalRead, ProfesionalCreate
from app.domain.models import DiaSemanaEnum
from backend.app.services.agenda_profesional_service import AgendaProfesionalService


router = APIRouter(prefix="/profesionales", tags=["Profesionales"])

@router.get("/{profesional_id}/horarios", response_model=list[HorarioProfesionalRead])
def obtener_horarios_profesional(
    profesional_id: int,
    service: HorarioProfesionalService = Depends(get_horario_profesional_service)
):
    try:
        return service.get_by_profesional(profesional_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{profesional_id}/horarios/{dia}", response_model=HorarioProfesionalRead | None)
def configurar_horario_dia_profesional(
    profesional_id: int, 
    dia: DiaSemanaEnum, 
    datos: HorarioDiaInput, # <--- FastAPI leerá esto del Body (JSON)
    service: HorarioProfesionalService = Depends(get_horario_profesional_service)
):
    try:
        # Llamamos al servicio pasando los datos ya validados y parseados
        return service.configurar_horario_dia(
            profesional_id=profesional_id,
            dia=dia,
            inicio=datos.hora_inicio,
            fin=datos.hora_fin,
            trabaja=datos.trabaja
        )
    except ValueError as e:
        # Capturamos errores de negocio (ej: profesional no existe)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/crear", response_model=ProfesionalRead | None)
def crear_profesional(
    profesional_data: ProfesionalCreate,
    service: ProfesionalService = Depends(get_profesional_service)
):
    try:
        return service.crear_profesional(profesional_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{profesional_id}", response_model=ProfesionalRead | None)
def obtener_profesional_por_id(
    profesional_id: int,
    service: ProfesionalService = Depends(get_profesional_service)
):
    try:
        profesional = service.profesional_repo.get_by_id(profesional_id)
        if not profesional:
            raise ValueError(f"No se encontró el profesional con ID {profesional_id}")
        return profesional
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.patch("/{profesional_id}/agenda/{agenda_id}/cancelar-turnos")
def cancelar_turnos_profesional(
    profesional_id: int,
    agenda_id: int,
    dias: list[int] = Body(...),
    service: AgendaProfesionalService = Depends(get_agenda_profesional_service)
):
    try:
        # Buscar la agenda del profesional
        agenda = service.agenda_repo.get_agenda_by_profesional_id(profesional_id)
        if not agenda:
            raise ValueError(f"No se encontró agenda para el profesional {profesional_id}")
        
        # Cancelar turnos con el ID correcto de la agenda
        service.cancelar_turnos(agenda_id, dias)
        
        return {
            "mensaje": f"Se cancelaron los turnos exitosamente",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

