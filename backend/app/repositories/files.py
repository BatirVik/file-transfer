from typing import Mapping, Protocol
from datetime import UTC, timedelta, datetime
from uuid import UUID

from sqlalchemy.orm import joinedload

from app.repositories.base import BaseRepository
from app.models.files import File, Folder


class FileInfo(Protocol):
    filename: str | None
    size: int | None


class FilesRepository(BaseRepository):
    async def create_folder(
        self, lifetime_minutes: int, files: Mapping[UUID, FileInfo]
    ) -> Folder:
        expire_at = datetime.now(UTC) + timedelta(minutes=lifetime_minutes)
        folder = Folder(expire_at=expire_at)
        folder.files = [
            File(id=id, filename=file.filename, size=file.size)
            for id, file in files.items()
        ]
        self.db.add(folder)
        await self.db.commit()
        return folder

    async def read_folder(
        self, folder_id: UUID, include_files: bool = False
    ) -> Folder | None:
        options = []
        if include_files:
            options.append(joinedload(Folder.files))
        return await self.db.get(Folder, folder_id, options=options)

    async def read_file(
        self, file_id: UUID, include_folder: bool = False
    ) -> File | None:
        options = []
        if include_folder:
            options.append(joinedload(File.folder))
        return await self.db.get(File, file_id, options=options)
