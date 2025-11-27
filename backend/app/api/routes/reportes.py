from fastapi import APIRouter, Depends, Query, HTTPException
from app.api.dependencies import get_reporte_service
from app.services import ReporteService
from app.domain.schemas import ReporteCantidadTurnoPorEspecialidad, ReporteTurnosPeriodo, ReporteMontoTurnoPorEspecialidad
from datetime import date

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/turnos-por-especialidad", response_model=None)
def reporte_cantidad_turnos_por_especialidad(service: ReporteService = Depends(get_reporte_service)):
    """
    Genera un PDF con el reporte de cantidad de turnos por especialidad
    """
    try:
        ruta_pdf = service.reporte_cantidad_turnos_especialidad()
        return {"mensaje": "PDF generado exitosamente", "ruta": ruta_pdf}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")


@router.get("/pacientes-por-obra-social", response_model=dict)
def reporte_pacientes_por_obra_social(service: ReporteService = Depends(get_reporte_service)):
    mensaje = "El reporte se ha generado correctamente y se encuentra en la carpeta 'reportes' del proyecto."
    ruta = service.reporte_pacientes_por_obra_social()

@router.get("/montos-por-especialidad", response_model=None)
def reporte_montos_por_especialidad(service: ReporteService = Depends(get_reporte_service)):
    """
    Genera un PDF con el reporte de montos por especialidad
    """
    try:
        ruta_pdf = service.reporte_montos_especialidad()
        return {"mensaje": "PDF generado exitosamente", "ruta": ruta_pdf}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")

@router.get("/turnos-por-periodo", response_model=None)
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

    try:
        ruta_pdf = service.generar_reporte_periodo(mes_inicio, mes_fin, anio)
        return {"mensaje": "PDF generado exitosamente", "ruta": ruta_pdf}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")

@router.get("/profesionales-por-especialidad", response_model=dict)
def reporte_profesionales_por_especialidad(service: ReporteService = Depends(get_reporte_service)):
    mensaje = "El reporte se ha generado correctamente y se encuentra en la carpeta 'reportes' del proyecto."
    ruta = service.reporte_profesionales_por_especialidad()
    return {"mensaje": mensaje,
            "ruta": ruta}