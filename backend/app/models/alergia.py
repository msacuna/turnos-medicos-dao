from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class Alergia(Base):
    __tablename__ = "alergia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)

    # Relaciones Many-to-Many
    pacientes = relationship(
        "Paciente",
        secondary="paciente_alergia", 
        back_populates="alergias"
    )