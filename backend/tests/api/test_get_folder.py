from pathlib import Path
from uuid import uuid4
from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.files import Folder

MOCK_DIR = Path(__file__).parent.parent / "mock"


def test_get_folder(db: AsyncSession, client: TestClient, db_folder: Folder):
    resp = client.get(f"v1/folders/{db_folder.id}")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data.keys() == {"id", "expireAt", "files"}

    expected_id = str(db_folder.id)
    assert expected_id == resp_data["id"]

    expire_at = datetime.fromisoformat(resp_data["expireAt"])
    assert db_folder.expire_at == expire_at

    resp_files = {(file["id"], file["filename"]) for file in resp_data["files"]}
    db_file = {(str(file.id), file.filename) for file in db_folder.files}
    assert resp_files == db_file


def test_get_expired_folder(
    db: AsyncSession, client: TestClient, db_expired_folder: Folder
):
    resp = client.get(f"v1/folders/{db_expired_folder.id}")
    assert resp.status_code == 410
    assert resp.json() == {"detail": "Folder is no longer available"}


def test_get_not_found_folder(db: AsyncSession, client: TestClient):
    resp = client.get(f"v1/folders/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Folder not found"}
