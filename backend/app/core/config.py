from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str
    APP_VERSION: str

    # Database
    DATABASE_URL: str

    # Authentication
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()