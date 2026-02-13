"""Core Configuration Module"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application Settings"""
    # --- Project Metadata ---
    API_V1_STR: str
    PROJECT_NAME: str
    PROJECT_VERSION: str
    DESCRIPTION: str

    # --- JWT ---
    JWT_ALGORITHM:str

    JWT_ACCESS_KEY:str
    JWT_ACCESS_TTL:int

    JWT_REFRESH_KEY:str
    JWT_REFRESH_TTL:int

    # --- Server Configuration ---
    HOST: str
    PORT: int
    DEBUG: bool
    RELOAD: bool

    # --- Database Configuration ---
    DATABASE_URL: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool

    # --- Security ---
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # --- CORS Configuration ---
    CORS_ORIGINS: list[str]

    model_config = {
        "env_file":".env",
        "case_sensitive":True
    }


settings = Settings()
