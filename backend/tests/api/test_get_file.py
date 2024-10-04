from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.files import Folder

MOCK_DIR = Path(__file__).parent.parent / "mock"


def test_get_file(db: AsyncSession, client: TestClient, db_folder: Folder):
    file = db_folder.files[0]
    resp = client.get(f"v1/files/{file.id}/download")
    assert resp.status_code == 200, resp.json()

    resp_file_length = 0
    for chunk in resp.iter_bytes():
        resp_file_length += len(chunk)

    content_lenght = resp.headers.get("Content-Length")
    assert int(content_lenght) == resp_file_length

    assert file.filename is not None, "db_folder fixture must attach filename"
    expected_file_length = (MOCK_DIR / file.filename).stat().st_size
    assert resp_file_length == expected_file_length


def test_get_expired_file(
    db: AsyncSession, client: TestClient, db_expired_folder: Folder
):
    file = db_expired_folder.files[0]
    resp = client.get(f"v1/files/{file.id}/download")
    assert resp.status_code == 410
    assert resp.json() == {"detail": "File is no longer available"}


def test_get_not_found_file(db: AsyncSession, client: TestClient, db_folder: Folder):
    resp = client.get(f"v1/files/{uuid4()}/download")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "File not found"}
