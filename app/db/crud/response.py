from app.db.crud.base import CRUDBase
from app.models.response import Response
from app.schemas.response import ResponseCreate

response_crud = CRUDBase[Response, ResponseCreate](Response)
