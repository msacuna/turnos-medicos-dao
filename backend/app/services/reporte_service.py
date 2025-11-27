from app.repositories import ReporteRepository
from app.domain.schemas import ReporteTurnoPorEspecialidad

class ReporteService:
    def __init__(self, repo: ReporteRepository):
        self.repo = repo

    def reporte_turnos_especialidad(self) -> list[ReporteTurnoPorEspecialidad]:
        resultados = self.repo.get_turno_por_especialidad()
        reportes = [ReporteTurnoPorEspecialidad.model_validate(r) for r in resultados]
        return reportes
    

    