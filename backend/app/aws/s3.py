from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import AsyncIterator

from types_aiobotocore_s3.client import S3Client
from types_aiobotocore_s3.service_resource import S3ServiceResource
from types_aiobotocore_s3.type_defs import FileobjTypeDef
from app.config import config

from .session import session


@asynccontextmanager
async def get_s3() -> AsyncGenerator[S3ServiceResource]:
    async with session.resource("s3", endpoint_url=config.AWS_ENDPOINT_URL) as s3:
        yield s3


@asynccontextmanager
async def get_s3_client() -> AsyncGenerator[S3Client]:
    async with session.client("s3", endpoint_url=config.AWS_ENDPOINT_URL) as s3:
        yield s3


async def upload_files(**files: FileobjTypeDef) -> None:
    async with get_s3() as resource:
        bucket = await resource.Bucket(config.S3_BUCKET_NAME)
        for filename, file_io in files.items():
            await bucket.upload_fileobj(file_io, filename)


async def download_file(filename: str) -> tuple[AsyncIterator[bytes], int]:
    length = 0

    async def gen_chunks() -> AsyncGenerator:
        async with get_s3_client() as client:
            resp = await client.get_object(Bucket=config.S3_BUCKET_NAME, Key=filename)
            yield resp["ContentLength"]
            async for chunk in resp["Body"].iter_chunks():
                yield chunk

    chunks = aiter(gen_chunks())
    length = await anext(chunks)
    return chunks, length
