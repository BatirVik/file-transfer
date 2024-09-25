from datetime import timedelta, datetime
from uuid import UUID

from typing import Iterable
from sqlalchemy import func

from app.repositories.base import BaseRepository
from app.models.files import File, Folder


class FolderRepository(BaseRepository):
    async def create_folder(
        self,
        filenames: Iterable[str],
        lifetime_minutes: int,
        folder_id: UUID | None = None,
    ) -> Folder:
        lifetime = timedelta(minutes=lifetime_minutes)
        expire_at = datetime.utcnow() + lifetime
        if folder_id is None:
            folder = Folder(expire_at=expire_at)
            await self.db.flush([folder])
        else:
            folder = Folder(id=folder_id, expire_at=expire_at)

        folder.files = [File(filename=name) for name in filenames]
        self.db.add(folder)
        await self.db.commit()
        return folder
