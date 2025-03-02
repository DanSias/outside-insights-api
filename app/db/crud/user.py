from sqlalchemy.orm import Session
from app.db.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate


class CRUDUser(CRUDBase[User, UserCreate]):
    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()


user_crud = CRUDUser(User)
