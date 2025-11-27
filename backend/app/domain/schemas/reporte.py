from pydantic import BaseModel, ConfigDict

class ReporteCantidadTurnoPorEspecialidad(BaseModel):
    especialidad: str
    cantidad_turnos: int


class ReporteMontoTurnoPorEspecialidad(BaseModel):
    especialidad: str
    monto_total: float

# Este representa una fila de tu consulta SQL (un estado)
class DetalleEstadoTurno(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    estado: str
    cantidad: int
    monto_estimado: float
    

# Este es el reporte final que recibe el Frontend
class ReporteTurnosPeriodo(BaseModel):
    anio: int
    mes_inicio: int
    mes_fin: int
    # Totales calculados en el servicio
    total_turnos: int
    total_ingresos_estimados: float
    # La lista desglosada
    detalles: list[DetalleEstadoTurno]