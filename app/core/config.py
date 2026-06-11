"""Core Configuration Module"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application Settings"""

    # --- Project Metadata ---
    API_V1_STR: str
    PROJECT_VERSION: str

    # --- JWT ---
    JWT_ALGORITHM: str

    JWT_ACCESS_KEY: str
    JWT_ACCESS_TTL: int

    JWT_REFRESH_KEY: str
    JWT_REFRESH_TTL: int

    # --- API_KEY_PREFIX ---
    PREFIX: str

    # --- Server Configuration ---
    DEBUG: bool

    # --- Database Configuration ---
    DATABASE_URL: str

    # --- Valkey Configuration ---
    VALKEY_HOST: str
    VALKEY_PORT:int

    # --- CORS Configuration ---
    CORS_ORIGINS: list[str]

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
