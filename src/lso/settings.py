from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # env
    LSO_ENV: str = "dev"

    # db
    LSO_DB_URL: str = "sqlite:///data/lso.db"

    # health thresholds (defaults from spec)
    LSO_OK_ERROR_RATE: float = 0.01
    LSO_OK_P95_MS: int = 800

    LSO_WARN_ERROR_RATE: float = 0.05
    LSO_WARN_P95_MS: int = 1500

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
