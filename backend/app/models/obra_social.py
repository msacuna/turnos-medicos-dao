from sqlalchemy import CheckConstraint, Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class ObraSocial(Base):
    __tablename__ = "obra_social"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    cuit = Column(String(11), nullable=False, unique=True)
    porcentaje_cobertura = Column(Numeric(5, 2), nullable=False) # Validar checks en schema
    id_tipo = Column(Integer, ForeignKey("tipo_obra_social.id"), nullable=False)

    __table_args__ = (
        CheckConstraint('porcentaje_cobertura >= 0', name='chk_porcentaje_cobertura_positiva'),
        CheckConstraint('porcentaje_cobertura <= 100', name='chk_porcentaje_cobertura_maximo'),
    )

    # Relaciones directas
    tipo = relationship("TipoObraSocial", back_populates="obras_sociales")
    obra_social_profesionales = relationship("ObraSocialProfesional", back_populates="obra_social")

    pacientes = relationship("Paciente", back_populates="obra_social")

    # Acceder directamente a los profesionales vigentes
    @property
    def profesionales_vigentes(self):
        return [osp.profesional for osp in self.obra_social_profesionales if osp.vigente]