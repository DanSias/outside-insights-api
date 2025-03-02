from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import Base

# Define generic types for SQLAlchemy model and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Base CRUD operations for SQLAlchemy models.

        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Retrieve a record by ID (UUID or int)"""
        return db.query(self.model).filter_by(id=id).first()

    def get_by_uuid(self, db: Session, uuid: str) -> Optional[ModelType]:
        """Retrieve a record by UUID"""
        return db.query(self.model).filter_by(uuid=uuid).first()

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Retrieve multiple records with pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        obj_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        """Update an existing record"""
        update_data = (
            obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        )
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: Any) -> Optional[ModelType]:
        """Delete a record by ID"""
        obj = db.query(self.model).filter_by(id=id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj
