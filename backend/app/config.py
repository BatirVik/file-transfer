import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Config(BaseSettings):
    DB_URL: PostgresDsn
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT_URL: str
    S3_BUCKET_NAME: str
    S3_REGION_NAME: str


match os.getenv("ENV"):
    case "production":
        dotenv_name = ".env"
    case "test":
        dotenv_name = ".env.test"
    case "development":
        dotenv_name = ".env.dev"
    case _ as env:
        raise ValueError(f"Unknown environment: {env}")

dotenv_path = Path(__file__).parent.parent / "configuration" / dotenv_name
config = Config(_env_file=dotenv_path)  # type: ignore
