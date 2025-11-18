from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    id_rol = Column(Integer, ForeignKey("rol.id"), nullable=False)

    # Relaciones directas
    rol = relationship("Rol", back_populates="usuarios")