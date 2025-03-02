from app.db.crud.base import CRUDBase
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate

organization_crud = CRUDBase[Organization, OrganizationCreate](Organization)
