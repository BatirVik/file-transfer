from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from loguru import logger
from types_aiobotocore_s3.client import S3Client
from aioboto3.session import Session
from types_aiobotocore_s3.type_defs import FileobjTypeDef


from app.config import config

session = Session(
    config.S3_ACCESS_KEY,
    config.S3_SECRET_KEY,
    region_name=config.S3_REGION_NAME,
)


@asynccontextmanager
async def get_client() -> AsyncGenerator[S3Client]:
    async with session.client("s3") as s3:
        yield s3


async def upload_folder(foldername: str, **files: FileobjTypeDef) -> None:
    async with get_client() as client:
        for filename, file_io in files.items():
            filename = f"{foldername}/{filename}"
            await client.upload_fileobj(file_io, config.S3_BUCKET_NAME, filename)
