# app/api/routes/profesionales.py
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_horario_profesional_service
from app.services import HorarioProfesionalService
from app.domain.schemas import HorarioProfesionalRead, HorarioDiaInput
from app.domain.models import DiaSemanaEnum

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