from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.files import Folder

MOCK_DIR = Path(__file__).parent.parent / "mock"


def test_get_file(db: AsyncSession, client: TestClient, db_folder: Folder):
    file = db_folder.files[0]
    resp = client.get(f"v1/files/{file.id}")

    assert resp.status_code == 200
    assert resp.json() == {
        "id": str(file.id),
        "folderId": str(file.folder_id),
        "size": file.size,
        "filename": file.filename,
    }


def test_get_expired_file(
    db: AsyncSession, client: TestClient, db_expired_folder: Folder
):
    file = db_expired_folder.files[0]
    resp = client.get(f"v1/files/{file.id}")
    assert resp.status_code == 410
    assert resp.json() == {"detail": "File is no longer available"}


def test_get_not_found_file(db: AsyncSession, client: TestClient, db_folder: Folder):
    resp = client.get(f"v1/files/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "File not found"}
