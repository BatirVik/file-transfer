from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.files import Folder

MOCK_DIR = Path(__file__).parent.parent / "mock"


def test_get_file(db: AsyncSession, client: TestClient, db_folder: Folder):
    filename = db_folder.files[0].filename
    resp = client.get(f"v1/files/folder/{db_folder.id}/{filename}")
    assert resp.status_code == 200
    resp_file_length = 0
    for chunk in resp.iter_bytes():
        resp_file_length += len(chunk)

    content_lenght = resp.headers.get("Content-Length")
    assert content_lenght is not None

    assert int(content_lenght) == resp_file_length

    expected_file_length = (MOCK_DIR / filename).stat().st_size
    assert resp_file_length == expected_file_length


def test_get_expired_file(
    db: AsyncSession, client: TestClient, db_expired_folder: Folder
):
    filename = db_expired_folder.files[0].filename
    resp = client.get(f"v1/files/folder/{db_expired_folder.id}/{filename}")
    assert resp.status_code == 410


def test_get_not_found_file(db: AsyncSession, client: TestClient, db_folder: Folder):
    resp = client.get(f"v1/files/folder/{db_folder.id}/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "File not found"}


def test_get_file_of_not_found_folder(
    db: AsyncSession, client: TestClient, db_folder: Folder
):
    resp = client.get(f"v1/files/folder/{uuid4()}/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Folder not found"}
