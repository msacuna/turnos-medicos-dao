from app.repositories import ReporteRepository
from app.domain.schemas import ReporteCantidadTurnoPorEspecialidad, ReporteTurnosPeriodo, DetalleEstadoTurno, ReporteMontoTurnoPorEspecialidad

class ReporteService:
    def __init__(self, repo: ReporteRepository):
        self.repo = repo

    def reporte_cantidad_turnos_especialidad(self) -> list[ReporteCantidadTurnoPorEspecialidad]:
        resultados = self.repo.get_cantidad_turnos_por_especialidad()
        reportes = [ReporteCantidadTurnoPorEspecialidad.model_validate(r) for r in resultados]
        return reportes
    
    def reporte_montos_especialidad(self) -> list[ReporteMontoTurnoPorEspecialidad]:
        resultados = self.repo.get_monto_turnos_por_especialidad()
        reportes = [ReporteMontoTurnoPorEspecialidad.model_validate(r) for r in resultados]
        return reportes
    
    def generar_reporte_periodo(self, mes_inicio: int, mes_fin: int, anio: int) -> ReporteTurnosPeriodo:
        # 1. Obtener datos crudos de la BD
        datos_crudos = self.repo.get_turnos_por_periodo(mes_inicio, mes_fin, anio)
        
        # 2. Variables acumuladoras
        total_turnos = 0
        total_ingresos = 0.0
        detalles_procesados = []

        # 3. Procesar cada fila
        for fila in datos_crudos:
            # Convertimos a objeto Pydantic
            item = DetalleEstadoTurno(
                estado=fila['estado'],
                cantidad=fila['cantidad'],
                monto_estimado=fila['monto_estimado']
            )
            
            # Acumulamos totales
            total_turnos += item.cantidad
            total_ingresos += item.monto_estimado
            
            detalles_procesados.append(item)

        # 4. Construir respuesta final
        return ReporteTurnosPeriodo(
            anio=anio,
            mes_inicio=mes_inicio,
            mes_fin=mes_fin,
            total_turnos=total_turnos,
            total_ingresos_estimados=total_ingresos,
            detalles=detalles_procesados)