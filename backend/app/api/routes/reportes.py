from fastapi import APIRouter, Depends, Query, HTTPException
from app.api.dependencies import get_reporte_service
from app.services import ReporteService
from app.domain.schemas import ReporteCantidadTurnoPorEspecialidad, ReporteTurnosPeriodo, ReporteMontoTurnoPorEspecialidad
from datetime import date

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/turnos-por-especialidad", response_model=list[ReporteCantidadTurnoPorEspecialidad])
def reporte_turnos_por_especialidad(service: ReporteService = Depends(get_reporte_service)):
    return service.reporte_cantidad_turnos_especialidad()

@router.get("/montos-por-especialidad", response_model=list[ReporteMontoTurnoPorEspecialidad])
def reporte_montos_por_especialidad(service: ReporteService = Depends(get_reporte_service)):
    return service.reporte_montos_especialidad()

@router.get("/turnos-por-periodo", response_model=ReporteTurnosPeriodo)
def obtener_reporte_turnos_periodo(
    anio: int = Query(default=None, description="Año del reporte"),
    mes_inicio: int = Query(default=1, ge=1, le=12),
    mes_fin: int = Query(default=12, ge=1, le=12),
    service: ReporteService = Depends(get_reporte_service)
):
    # Si no envían año, usamos el actual
    if anio is None:
        anio = date.today().year
        
    if mes_inicio > mes_fin:
        raise HTTPException(status_code=400, detail="El mes de inicio no puede ser mayor al mes de fin")

    return service.generar_reporte_periodo(mes_inicio, mes_fin, anio)