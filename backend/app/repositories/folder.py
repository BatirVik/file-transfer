from uuid import UUID

from app.repositories.base import BaseRepository
from typing import Iterable

from app.models.files import File, Folder


class FolderRepository(BaseRepository):
    async def create_folder(
        self, filenames: Iterable[str], folder_id: UUID | None = None
    ) -> Folder:
        if folder_id is None:
            folder = Folder()
            await self.db.flush([folder])
        else:
            folder = Folder(folder_id=folder_id)

        folder.files = [File(filename=name) for name in filenames]
        self.db.add(folder)
        await self.db.flush()
        return folder
