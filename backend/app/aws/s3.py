from collections.abc import AsyncGenerator, AsyncIterator, Iterable, Mapping
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO

from botocore.exceptions import ClientError

if TYPE_CHECKING:
    from types_aiobotocore_s3.client import S3Client
    from types_aiobotocore_s3.service_resource import S3ServiceResource
    from types_aiobotocore_s3.type_defs import FileobjTypeDef

from app.config import config

from .session import session


@asynccontextmanager
async def get_s3_resource() -> AsyncGenerator["S3ServiceResource"]:
    async with session.resource("s3", endpoint_url=config.AWS_ENDPOINT_URL) as s3:
        yield s3


@asynccontextmanager
async def get_s3_client() -> AsyncGenerator["S3Client"]:
    async with session.client("s3", endpoint_url=config.AWS_ENDPOINT_URL) as s3:
        yield s3


async def create_bucket(bucket_name: str) -> None:
    async with get_s3_client() as client:
        await client.create_bucket(Bucket=config.S3_BUCKET_NAME)


async def clear_bucket(bucket_name: str) -> None:
    async with get_s3_resource() as resource:
        bucket = await resource.Bucket(config.S3_BUCKET_NAME)
        await bucket.objects.all().delete()


async def upload_files(**files: "FileobjTypeDef") -> None:
    async with get_s3_client() as client:
        for filename, file_io in files.items():
            await client.upload_fileobj(
                file_io, Bucket=config.S3_BUCKET_NAME, Key=filename
            )


async def download_file(filename: str) -> tuple[AsyncIterator[bytes], int]:
    async def gen_chunks() -> AsyncGenerator:
        async with get_s3_client() as client:
            resp = await client.get_object(Bucket=config.S3_BUCKET_NAME, Key=filename)
            yield resp["ContentLength"]
            async for chunk in resp["Body"].iter_chunks():
                yield chunk

    chunks = aiter(gen_chunks())
    length = await anext(chunks)
    return chunks, length


async def download_files_zip(filenames: Mapping[str, str]) -> AsyncIterator[bytes]:
    zip_stream = BytesIO()
    with ZipFile(zip_stream, "w", ZIP_DEFLATED) as zip_file:
        for s3_filename, zip_filename in filenames.items():
            chunks, _ = await download_file(s3_filename)
            with zip_file.open(zip_filename, "w") as dest:
                async for chunk in chunks:
                    dest.write(chunk)
                    yield zip_stream.read()
                    zip_stream.truncate()
    zip_stream.seek(0)
    yield zip_stream.read()


async def delete_files(filenames: Iterable[str]) -> dict[str, ClientError | None]:
    exceptions: dict[str, ClientError | None] = {}
    async with get_s3_client() as client:
        for filename in filenames:
            try:
                await client.delete_object(Bucket=config.S3_BUCKET_NAME, Key=filename)
                exceptions[filename] = None
            except ClientError as e:
                exceptions[filename] = e
    return exceptions
