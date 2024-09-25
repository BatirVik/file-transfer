import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.files import Folder

MOCK_DIR = Path(__file__).parent.parent / "mock"


@pytest.mark.asyncio
async def test_upload_files(db: AsyncSession, client: TestClient):
    filenames = os.listdir(MOCK_DIR)
    files = [("files", (name, open(MOCK_DIR / name, "rb"))) for name in filenames]
    resp = client.post("/files/folder", files=files)
    assert resp.status_code == 201
    resp_data = resp.json()
    assert resp_data.keys() == {"id"}

    folder = await db.get(Folder, resp_data["id"], options=[joinedload(Folder.files)])
    assert folder

    assert {file.filename for file in folder.files} == set(filenames)


@pytest.mark.asyncio
async def test_upload_files_with_duplicate_names(db: AsyncSession, client: TestClient):
    files = [
        ("files", ("image.jpg", open(MOCK_DIR / name, "rb")))
        for name in os.listdir(MOCK_DIR)
    ]
    resp = client.post("/files/folder", files=files)
    assert resp.status_code == 400, resp.json()
    assert resp.json() == {"detail": "All files must have a unique filename"}


@pytest.mark.asyncio
async def test_upload_zero_files(db: AsyncSession, client: TestClient):
    resp = client.post("/files/folder", files=[])
    assert resp.status_code == 422
