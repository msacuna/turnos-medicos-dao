from typing import Generic, TypeVar, Optional, Any
from sqlmodel import Session, select
from app.core.database import db

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T], session: Session):
        self.model = model
        self.session = session
    
    def get_all(self) -> list[T]:
        statement = select(self.model)
        result = self.session.exec(statement)
        return list(result.all())
    
    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)
    
    def add(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity
    
    def update(self, entity: T, new_data: dict | None = None) -> T:
        if new_data:
            for key, value in new_data.items():
                setattr(entity, key, value)
        
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity
    
    def delete(self, id: Any) -> bool:
        entity = self.session.get(self.model, id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return True
        return False