from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    TMDB_API_TOKEN: str
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    DEFAULT_REGION: str = "FR"
    DEFAULT_LANGUAGE: str = "fr-FR"
    CACHE_TTL_SECONDS: int = 900


settings = Settings()