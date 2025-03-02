from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.security import get_current_user
from app.db.session import engine, Base
from app.core.logging import configure_logging

# Create the FastAPI app
app = FastAPI(
    title="AI API Backend",
    description="API backend for proxying requests to various LLM providers",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
configure_logging()

# Include API router
app.include_router(api_router, prefix="/api/v1")


# Create database tables on startup
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
