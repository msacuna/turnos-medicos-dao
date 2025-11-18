from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Profesional(Base):
    __tablename__ = 'profesional'

    id = Column(Integer, primary_key=True, autoincrement=True)
    matricula = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefono = Column(String(20), nullable=False)

    id_especialidad = Column(Integer, ForeignKey("especialidad.id"), nullable=False)

    # Relaciones directas
    especialidad = relationship("Especialidad", back_populates="profesionales")
    obra_social_profesionales = relationship("ObraSocialProfesional", back_populates="profesional")
    horario_profesionales = relationship("HorarioProfesional", back_populates="profesional")

    agendas_profesionales = relationship("AgendaProfesional", back_populates="profesional")

    # Acceder directamente a las obras sociales vigentes
    @property
    def obras_sociales_vigentes(self):
        return [osp.obra_social for osp in self.obra_social_profesionales if osp.vigente]
    
    # Acceder directamente al horario vigente del profesional
    @property
    def horarios_vigentes(self):
        return [hp.horario_atencion for hp in self.horario_profesionales if hp.vigente]