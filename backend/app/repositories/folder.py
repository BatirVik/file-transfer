from datetime import UTC, timedelta, datetime
from uuid import UUID

from typing import Iterable
from sqlalchemy.orm import joinedload

from app.repositories.base import BaseRepository
from app.models.files import File, Folder


class FilesRepository(BaseRepository):
    async def create_folder(
        self,
        filenames: Iterable[str],
        lifetime_minutes: int,
        folder_id: UUID | None = None,
    ) -> Folder:
        lifetime = timedelta(minutes=lifetime_minutes)
        expire_at = datetime.now(UTC) + lifetime
        if folder_id is None:
            folder = Folder(expire_at=expire_at)
            await self.db.flush([folder])
        else:
            folder = Folder(id=folder_id, expire_at=expire_at)
        folder.files = [File(filename=name) for name in filenames]
        self.db.add(folder)
        await self.db.commit()
        return folder

    async def get_folder(
        self, folder_id: UUID, files_include: bool = False
    ) -> Folder | None:
        options = []
        if files_include:
            options.append(joinedload(Folder.files))
        return await self.db.get(Folder, folder_id, options=options)
