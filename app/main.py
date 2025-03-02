from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="Outside Insights API", version="1.0")

# Include API routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Outside Insights API is running!"}
