from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "TrustHire API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    POSTGRES_DB: str = "trusthire"
    POSTGRES_USER: str = "trusthire"
    POSTGRES_PASSWORD: str = "trusthire"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    model_config = SettingsConfigDict(
        case_sensitive=True
    )


settings = Settings()