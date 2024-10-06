from io import BytesIO
import os
from pathlib import Path
from uuid import uuid4
from zipfile import ZIP_DEFLATED, ZipFile

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.files import Folder

MOCK_DIR = Path(__file__).parent.parent / "mock"


def test_download_folder(db: AsyncSession, client: TestClient, db_folder: Folder):
    resp = client.get(f"v1/folders/{db_folder.id}/download")
    assert resp.status_code == 200
    # bytes = resp.read()
    # input(bytes)
    file = BytesIO(resp.read())
    file.seek(0)
    with ZipFile(file, compression=ZIP_DEFLATED) as zip_file:
        resp_filenames = set(zip_file.namelist())
        expected_filenames = set(os.listdir(MOCK_DIR))
        assert resp_filenames == expected_filenames
        for filename in resp_filenames:
            assert zip_file.read(filename) == open(MOCK_DIR / filename, "rb").read()


def test_download_expired_folder(
    db: AsyncSession, client: TestClient, db_expired_folder: Folder
):
    resp = client.get(f"v1/folders/{db_expired_folder.id}/download")
    assert resp.status_code == 410
    assert resp.json() == {"detail": "Folder is no longer available"}


def test_download_not_found_folder(
    db: AsyncSession, client: TestClient, db_folder: Folder
):
    resp = client.get(f"v1/folders/{uuid4()}/download")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Folder not found"}
