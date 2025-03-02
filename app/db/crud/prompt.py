from sqlalchemy.orm import Session
from app.db.crud.base import CRUDBase
from app.models.prompt import Prompt
from app.schemas.prompt import PromptCreate


class CRUDPrompt(CRUDBase[Prompt, PromptCreate]):
    def get_prompts_by_user(self, db: Session, user_id):
        return db.query(Prompt).filter(Prompt.user_id == user_id).all()


prompt_crud = CRUDPrompt(Prompt)
