from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class TipoObraSocial(Base):
    __tablename__ = "tipo_obra_social"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    # Relaciones inversas
    obras_sociales = relationship("ObraSocial", back_populates="tipo")