from sqlmodel import text
from app.core.database import db

class ReporteRepository:
    def __init__(self):
        pass

    @property
    def session(self):
        return db.get_session

    def get_turno_por_especialidad(self) -> list[dict]:
        # SQL puro
        query = text("""
            SELECT e.nombre AS especialidad, COUNT(t.id) AS cantidad_turnos
            FROM especialidad e
            JOIN turno t ON t.id_especialidad = e.id
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
