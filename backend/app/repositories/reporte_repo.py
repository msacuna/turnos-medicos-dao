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