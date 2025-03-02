from app.db.crud.base import CRUDBase
from app.models.llm_provider import LLMProvider
from app.schemas.llm_provider import LLMProviderCreate

llm_provider_crud = CRUDBase[LLMProvider, LLMProviderCreate](LLMProvider)
