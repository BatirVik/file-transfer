from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.files import Folder

MOCK_DIR = Path(__file__).parent.parent / "mock"


def test_get_folder(db: AsyncSession, client: TestClient, db_folder: Folder):
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


def test_get_expired_folder(
    db: AsyncSession, client: TestClient, db_expired_folder: Folder
):
    resp = client.get(f"v1/files/folder/{db_expired_folder.id}")
    assert resp.status_code == 410


def test_get_not_found_folder(db: AsyncSession, client: TestClient):
    resp = client.get(f"v1/files/folder/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Folder not found"}
