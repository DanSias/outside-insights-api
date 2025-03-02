from app.db.crud.base import CRUDBase
from app.models.team import Team
from app.schemas.team import TeamCreate

team_crud = CRUDBase[Team, TeamCreate](Team)
