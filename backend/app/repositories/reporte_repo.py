from sqlmodel import text
from app.core.database import db

class ReporteRepository:
    def __init__(self):
        pass

    @property
    def session(self):
        return db.get_session

    def get_cantidad_turnos_por_especialidad(self) -> list[dict]:
        # SQL puro
        query = text("""
            SELECT e.nombre AS especialidad, COUNT(t.id) AS cantidad_turnos
            FROM especialidad e
            LEFT JOIN turno t ON t.id_especialidad = e.id
            GROUP BY e.nombre
            ORDER BY cantidad_turnos DESC
        """)

        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]

    def get_paciente_por_obra_social(self) -> list[dict]:
        # SQL puro
        query = text("""
            SELECT os.nombre AS obra_social, 
                   COUNT(p.dni) AS cantidad_pacientes, 
                   COALESCE(SUM(t.monto), 0) AS monto_total_turnos
            FROM obra_social os
            LEFT JOIN paciente p ON p.nombre_obra_social = os.nombre
            LEFT JOIN turno t ON t.dni_paciente = p.dni
            GROUP BY os.nombre
            ORDER BY cantidad_pacientes DESC
        """)

        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]
    
    def get_monto_turnos_por_especialidad(self) -> list[dict]:
        query = text("""
            SELECT e.nombre AS especialidad, COALESCE(SUM(t.monto), 0) AS monto_total
            FROM especialidad e
            LEFT JOIN turno t ON t.id_especialidad = e.id
            GROUP BY e.nombre
            ORDER BY monto_total DESC
        """)

        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]
    
    def get_turnos_por_periodo(self, mes_inicio: int, mes_fin: int, anio: int) -> list[dict]:
        """
        Retorna un resumen de turnos en un periodo agrupados por estado, con montos y cantidades.
        """
        query = text("""
            SELECT 
                et.nombre AS estado,
                COUNT(t.id) AS cantidad,
                COALESCE(SUM(t.monto), 0) AS monto_estimado
            FROM estados_turno et
            LEFT JOIN turno t ON 
                t.nombre_estado = et.nombre AND
                EXTRACT(MONTH FROM t.fecha) BETWEEN :mes_inicio AND :mes_fin AND
                EXTRACT(YEAR FROM t.fecha) = :anio
            GROUP BY et.nombre
            ORDER BY cantidad DESC
        """)

        result = self.session.execute(
            query,
            # Se pasa la query anterior + los siguientes parámetros
            {"mes_inicio": mes_inicio, "mes_fin": mes_fin, "anio": anio}
            )
        return [row._asdict() for row in result.fetchall()]
    
    def get_turnos_por_periodo_mensual(self, mes_inicio: int, mes_fin: int, anio: int) -> list[dict]:
        """
        Retorna turnos agrupados por mes y estado para el gráfico de líneas.
        """
        query = text("""
            SELECT 
                EXTRACT(MONTH FROM t.fecha) AS mes,
                t.nombre_estado AS estado,
                COUNT(t.id) AS cantidad
            FROM turno t
            WHERE 
                EXTRACT(MONTH FROM t.fecha) BETWEEN :mes_inicio AND :mes_fin
                AND EXTRACT(YEAR FROM t.fecha) = :anio
            GROUP BY EXTRACT(MONTH FROM t.fecha), t.nombre_estado
            ORDER BY mes, estado
        """)

        result = self.session.execute(
            query,
            {"mes_inicio": mes_inicio, "mes_fin": mes_fin, "anio": anio}
        )
        return [row._asdict() for row in result.fetchall()]
    def get_profesional_por_especialidad(self) -> list[dict]:
        # SQL puro
        
        query = text("""
            SELECT e.nombre AS especialidad, 
                   GROUP_CONCAT(CONCAT(pr.nombre, ' ', pr.apellido) SEPARATOR ', ') AS nombres_profesionales,
                   COUNT(pr.id) AS cantidad_profesionales
            FROM especialidad e
            LEFT JOIN profesional pr ON pr.id_especialidad = e.id
            GROUP BY e.nombre
            ORDER BY cantidad_profesionales DESC
        """)

        result = self.session.execute(query)
        return [row._asdict() for row in result.fetchall()]