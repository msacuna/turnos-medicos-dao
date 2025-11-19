from typing import Generic, TypeVar, Optional, Any
from sqlmodel import SQLModel, Session, select

T = TypeVar("T", bound=SQLModel) # Solo permisible para tipos de la bd

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        """Recibe sesión de DB y el modelo SQLModel asociado."""
        self.session = session
        self.model = model

    def get_all(self) -> list[T]:
        statement = select(self.model)
        return self.session.exec(statement).all() # type: ignore
    
    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)
    
    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity) # Recarga el objeto en la bd
        return entity
    
    def update(self, db_entity: T, json_data: dict) -> T:
        for key, value in json_data.items():
            if hasattr(db_entity, key): 
                setattr(db_entity, key, value) # Actualiza solo si el atributo existe
        
        self.session.add(db_entity)
        self.session.commit()
        self.session.refresh(db_entity)
        return db_entity
    
    def delete(self, id: Any) -> bool:
        entity = self.session.get(self.model, id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False