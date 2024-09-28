from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from io import BytesIO

from types_aiobotocore_s3.client import S3Client
from types_aiobotocore_s3.service_resource import S3ServiceResource
from types_aiobotocore_s3.type_defs import FileobjTypeDef
from aioboto3.session import Session

from app.config import config

session = Session(
    config.AWS_ACCESS_KEY,
    config.AWS_SECRET_KEY,
    region_name=config.AWS_REGION_NAME,
)


@asynccontextmanager
async def get_client() -> AsyncGenerator[S3Client]:
    async with session.client("s3", endpoint_url=config.AWS_ENDPOINT_URL) as s3:
        yield s3


@asynccontextmanager
async def get_resource() -> AsyncGenerator[S3ServiceResource]:
    async with session.resource("s3", endpoint_url=config.AWS_ENDPOINT_URL) as s3:
        yield s3


async def upload_folder(foldername: str, **files: FileobjTypeDef) -> None:
    async with get_resource() as resource:
        bucket = await resource.Bucket(config.S3_BUCKET_NAME)
        for filename, file_io in files.items():
            filename = f"{foldername}/{filename}"
            await bucket.upload_fileobj(file_io, filename)


async def download_file(foldername: str, filename: str) -> tuple[BytesIO, int]:
    async with get_resource() as resource:
        bucket = await resource.Bucket(config.S3_BUCKET_NAME)
        stream = BytesIO()
        obj = await bucket.Object(f"{foldername}/{filename}")
        await obj.download_fileobj(stream)
        stream.seek(0)
        return stream, await obj.content_length
