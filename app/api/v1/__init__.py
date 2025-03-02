from fastapi import APIRouter

api_router = APIRouter()

# Import API endpoints
from app.api.v1.endpoints import (
    users,
    organizations,
    prompts,
    responses,
    llm_providers,
    teams,
)

# Include routers
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(
    organizations.router, prefix="/organizations", tags=["Organizations"]
)
api_router.include_router(prompts.router, prefix="/prompts", tags=["Prompts"])
api_router.include_router(responses.router, prefix="/responses", tags=["Responses"])
api_router.include_router(
    llm_providers.router, prefix="/llm_providers", tags=["LLM Providers"]
)
api_router.include_router(teams.router, prefix="/teams", tags=["Teams"])

__all__ = ["api_router"]
