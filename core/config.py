from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ns_api_key: str
    database_url: str
    poll_interval_seconds: int = 300

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()