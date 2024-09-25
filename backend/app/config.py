import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Config(BaseSettings):
    DB_URL: PostgresDsn

    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION_NAME: str
    AWS_ENDPOINT_URL: str
    S3_BUCKET_NAME: str


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
