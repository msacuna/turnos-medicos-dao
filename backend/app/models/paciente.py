from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Paciente(Base):
    __tablename__ = 'paciente'

    dni = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefono = Column(String(20), nullable=False)
    id_grupo_sanguineo = Column(Integer, ForeignKey("grupo_sanguineo.id"), nullable=False)
    id_obra_social = Column(Integer, ForeignKey("obra_social.id"), nullable=True)

    # Relaciones directas
    grupo_sanguineo = relationship("GrupoSanguineo", back_populates="pacientes")
    obra_social = relationship("ObraSocial", back_populates="pacientes")

    # Relaciones Many-to-Many
    alergias = relationship(
        "Alergia",
        secondary="paciente_alergia",
        back_populates="pacientes"
    )
    
    antecedentes = relationship(
        "Antecedente", 
        secondary="paciente_antecedente",
        back_populates="pacientes"
    )

    turnos = relationship("Turno", back_populates="paciente")