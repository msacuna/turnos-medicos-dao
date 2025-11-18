from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models import Base

# Tabla intermedia para relacion Many-to-Many entre Medicamento y Laboratorio
medicamento_laboratorio = Table(
    'medicamento_laboratorio',
    Base.metadata,
    Column('id_medicamento', Integer, ForeignKey('medicamento.id'), primary_key=True),
    Column('id_laboratorio', Integer, ForeignKey('laboratorio.id'), primary_key=True)
)

# Tabla intermedia para relacion Many-to-Many entre Paciente y Alergia
paciente_alergia = Table(
    'paciente_alergia',
    Base.metadata,
    Column('dni_paciente', Integer, ForeignKey('paciente.dni'), primary_key=True),
    Column('id_alergia', Integer, ForeignKey('alergia.id'), primary_key=True)
)

# Tabla intermedia para relacion Many-to-Many entre Paciente y Antecedente
paciente_antecedente = Table(
    'paciente_antecedente',
    Base.metadata,
    Column('dni_paciente', Integer, ForeignKey('paciente.dni'), primary_key=True),
    Column('id_antecedente', Integer, ForeignKey('antecedente.id'), primary_key=True)
)

# Tabla intermedia para relacion Many-to-Many entre Profesional y HorarioAtencion
class HorarioProfesional(Base):
    __tablename__ = "horario_profesional"

    id_profesional = Column(Integer, ForeignKey("profesional.id"), primary_key=True)
    id_horario_atencion = Column(Integer, ForeignKey("horario_atencion.id"), primary_key=True)
    vigente = Column(Boolean, nullable=False, default=True)

    # Relaciones hacia las entidades principales
    profesional = relationship("Profesional", back_populates="horario_profesionales")
    horario_atencion = relationship("HorarioAtencion", back_populates="horario_profesionales")


# Tabla intermedia para relacion Many-to-Many entre ObraSocial y Profesional
class ObraSocialProfesional(Base):
    __tablename__ = "obra_social_profesional"

    id_obra_social = Column(Integer, ForeignKey("obra_social.id"), primary_key=True)
    id_profesional = Column(Integer, ForeignKey("profesional.id"), primary_key=True)
    vigente = Column(Boolean, nullable=False, default=True)

    # Relaciones hacia las entidades principales
    obra_social = relationship("ObraSocial", back_populates="obra_social_profesionales")
    profesional = relationship("Profesional", back_populates="obra_social_profesionales")