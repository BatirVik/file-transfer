import os
from pathlib import Path
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.files import Folder

MOCK_DIR = Path(__file__).parent.parent / "mock"


@pytest.mark.asyncio
async def test_upload_files(db: AsyncSession, client: TestClient):
    filenames = set(os.listdir(MOCK_DIR))
    files = [("files", (name, open(MOCK_DIR / name, "rb"))) for name in filenames]
    resp = client.post("v1/folders", files=files, data={"lifetimeMinutes": "10"})
    assert resp.status_code == 201
    resp_data = resp.json()
    assert resp_data.keys() == {"id", "expireAt", "files"}

    folder = await db.get(Folder, resp_data["id"], options=[joinedload(Folder.files)])
    assert folder

    expire_at = datetime.fromisoformat(resp_data["expireAt"])
    assert folder.expire_at == expire_at

    expected_expire_at = datetime.now(UTC) + timedelta(minutes=10)
    assert abs(expected_expire_at - expire_at) < timedelta(minutes=1)

    resp_files = {
        (file["id"], file["filename"], file["size"]) for file in resp_data["files"]
    }
    db_file = {(str(file.id), file.filename, file.size) for file in folder.files}
    assert resp_files == db_file


def test_upload_zero_files(db: AsyncSession, client: TestClient):
    resp = client.post("v1/folders", files=[])
    assert resp.status_code == 422
