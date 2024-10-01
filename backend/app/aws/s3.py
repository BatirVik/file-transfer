from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from io import BytesIO

from types_aiobotocore_s3.service_resource import S3ServiceResource
from types_aiobotocore_s3.type_defs import FileobjTypeDef
from app.config import config

from .session import session


@asynccontextmanager
async def get_s3() -> AsyncGenerator[S3ServiceResource]:
    async with session.resource("s3", endpoint_url=config.AWS_ENDPOINT_URL) as s3:
        yield s3


async def upload_files(**files: FileobjTypeDef) -> None:
    async with get_s3() as resource:
        bucket = await resource.Bucket(config.S3_BUCKET_NAME)
        for filename, file_io in files.items():
            await bucket.upload_fileobj(file_io, filename)


async def download_file(filename: str) -> tuple[BytesIO, int]:
    async with get_s3() as resource:
        bucket = await resource.Bucket(config.S3_BUCKET_NAME)
        stream = BytesIO()
        obj = await bucket.Object(filename)
        await obj.download_fileobj(stream)
        stream.seek(0)
        return stream, await obj.content_length
