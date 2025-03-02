from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    organizations,
    teams,
    prompts,
    responses,
    llm_providers,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    organizations.router, prefix="/organizations", tags=["organizations"]
)
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(responses.router, prefix="/responses", tags=["responses"])
api_router.include_router(
    llm_providers.router, prefix="/llm-providers", tags=["llm-providers"]
)
