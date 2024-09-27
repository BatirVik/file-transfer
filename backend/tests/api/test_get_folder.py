import os
from pathlib import Path
from uuid import uuid4
from loguru import logger

from fastapi import UploadFile
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.files import Folder
from app.database import session_factory
from app.services.folder import FilesService

MOCK_DIR = Path(__file__).parent.parent / "mock"


@pytest_asyncio.fixture
async def db_folder() -> Folder:
    files = (open(MOCK_DIR / name, "rb") for name in os.listdir(MOCK_DIR))
    upload_files = [UploadFile(file, filename=file.name) for file in files]
    async with session_factory() as db:
        file_service = FilesService(db, logger)
        return await file_service.create_folder(upload_files, 5)


@pytest.mark.asyncio
async def test_get_folder(db: AsyncSession, client: TestClient, db_folder: Folder):
    resp = client.get(f"v1/files/folder/{db_folder.id}")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data.keys() == {"id", "expire_at", "files"}

    expected_files = {file.filename for file in db_folder.files}
    assert expected_files == set(resp_data["files"])

    expected_id = str(db_folder.id)
    assert expected_id == resp_data["id"]

    expected_expire_at = db_folder.expire_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert expected_expire_at == resp_data["expire_at"]


@pytest.mark.asyncio
async def test_get_not_found_folder(db: AsyncSession, client: TestClient):
    resp = client.get(f"v1/files/folder/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Folder not found"}
