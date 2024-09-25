from typing import AsyncGenerator
import os

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

os.environ["ENV"] = "test"

from app.config import config
from app.main import app
from app.database import session_factory, engine
from app.models.base import Base
from app.aws import s3


@pytest_asyncio.fixture(autouse=True)
async def db_life():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        yield
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()


@pytest_asyncio.fixture(autouse=True)
async def aws_life():
    async with s3.get_resource() as resource:
        bucket = await resource.create_bucket(Bucket=config.S3_BUCKET_NAME)
        yield
        await bucket.objects.all().delete()
        await bucket.delete()


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as db:
        yield db


@pytest.fixture
def client(db: AsyncSession) -> TestClient:
    return TestClient(app)


def test_1():
    pass
