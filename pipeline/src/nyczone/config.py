from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NYC_ZONING_", env_file=".env")

    app_token: str = ""
    db_path: Path = Path("data/cache/nyc.sqlite")
    cache_dir: Path = Path("data/cache")
    log_dir: Path = Path("data/logs")
    footprints_ttl_days: int = 7
    zoning_ttl_days: int = 30
    socrata_limit: int = 1000
    max_features: int = 50_000


settings = Settings()
