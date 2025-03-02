import os
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, Field, PostgresDsn, validator
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Settings(BaseSettings):
    """
    Application Configuration for FastAPI.
    """

    # API Base Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI API Backend"

    # Security & Authentication
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        60 * 24 * 8, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    ALGORITHM: str = Field("HS256", env="ALGORITHM")

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=[], env="BACKEND_CORS_ORIGINS"
    )

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(f"Invalid CORS format: {v}")

    # Database Configuration
    POSTGRES_SERVER: str = Field(..., env="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    DATABASE_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Assemble the Postgres DSN string dynamically."""
        if isinstance(v, str):
            return v
        return f"postgresql://{values['POSTGRES_USER']}:{values['POSTGRES_PASSWORD']}@{values['POSTGRES_SERVER']}/{values['POSTGRES_DB']}"

    # LLM API Configurations
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    OPENAI_API_BASE_URL: str = Field(
        "https://api.openai.com/v1", env="OPENAI_API_BASE_URL"
    )

    ANTHROPIC_API_KEY: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    ANTHROPIC_API_BASE_URL: str = Field(
        "https://api.anthropic.com/v1", env="ANTHROPIC_API_BASE_URL"
    )

    COHERE_API_KEY: Optional[str] = Field(None, env="COHERE_API_KEY")
    COHERE_API_BASE_URL: str = Field(
        "https://api.cohere.ai/v1", env="COHERE_API_BASE_URL"
    )

    GEMINI_API_KEY: Optional[str] = Field(None, env="GEMINI_API_KEY")
    GEMINI_API_BASE_URL: str = Field(
        "https://generativelanguage.googleapis.com/v1beta", env="GEMINI_API_BASE_URL"
    )

    DEEPSEEK_API_KEY: Optional[str] = Field(None, env="DEEPSEEK_API_KEY")
    DEEPSEEK_API_BASE_URL: str = Field(
        "https://api.deepseek.com/v1", env="DEEPSEEK_API_BASE_URL"
    )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
