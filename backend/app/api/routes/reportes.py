from fastapi import APIRouter, Depends
from app.api.dependencies import get_reporte_service
from app.services import ReporteService, reporte_service
from app.domain.schemas import ReporteTurnoPorEspecialidad

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/turnos-por-especialidad", response_model=list[ReporteTurnoPorEspecialidad])
def reporte_turnos_por_especialidad(service: ReporteService = Depends(get_reporte_service)):
    return service.reporte_turnos_especialidad()


@router.get("/turnos-por-especialidad", response_model=None)
