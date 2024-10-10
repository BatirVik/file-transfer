from pathlib import Path
from typing import AsyncGenerator
from datetime import UTC, datetime, timedelta
import os

from fastapi import UploadFile
from loguru import logger
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession


os.environ["ENV"] = "test"

from app.models.files import Folder
from app.services.files import FilesService
from app.config import config
from app.main import app
from app.database import session_factory, engine
from app.models.base import Base
from app.aws import logs, s3


@pytest_asyncio.fixture(autouse=True)
async def db_life():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        yield
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()


@pytest_asyncio.fixture(autouse=True)
async def aws_s3_life():
    await s3.create_bucket(config.S3_BUCKET_NAME)
    yield
    await s3.clear_bucket(config.S3_BUCKET_NAME)


@pytest_asyncio.fixture(autouse=True)
async def aws_logs_life():
    await logs.create_log_group(config.LOGS_LOG_GROUP_NAME)
    yield
    await logs.delete_log_group(config.LOGS_LOG_GROUP_NAME)


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as db:
        yield db


@pytest.fixture
def client(db: AsyncSession) -> TestClient:
    return TestClient(app)


@pytest.fixture
def files_service(db: AsyncSession) -> FilesService:
    return FilesService(db, logger)


MOCK_DIR = Path(__file__).parent / "mock"


@pytest_asyncio.fixture
async def db_folder(files_service: FilesService) -> Folder:
    files = {name: open(MOCK_DIR / name, "rb") for name in os.listdir(MOCK_DIR)}
    upload_files = [UploadFile(file, filename=name) for name, file in files.items()]
    return await files_service.create_folder(upload_files, 5)


@pytest_asyncio.fixture
async def db_expired_folder(files_service: FilesService) -> Folder:
    files = {name: open(MOCK_DIR / name, "rb") for name in os.listdir(MOCK_DIR)}
    upload_files = [UploadFile(file, filename=name) for name, file in files.items()]
    folder = await files_service.create_folder(upload_files, 5)
    folder.expire_at = datetime.now(UTC) - timedelta(days=10)
    await files_service.db.commit()
    return folder
