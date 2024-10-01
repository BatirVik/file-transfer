from collections.abc import Iterable
from datetime import UTC, datetime
from uuid import uuid4, UUID

from fastapi import UploadFile
from fastapi.responses import StreamingResponse

from app.aws import s3
from app.exceptions.files import (
    FileNotFound,
    FolderExpired,
    FolderNotFound,
)
from app.repositories.files import FilesRepository
from app.models.files import Folder

from .base import BaseService


class FilesService(BaseService[FilesRepository]):
    repository_cls = FilesRepository

    async def create_folder(
        self, files: Iterable[UploadFile], lifetime_minutes: int
    ) -> Folder:
        files_data = {uuid4(): file for file in files}

        s3_files_data = {str(id): file.file for id, file in files_data.items()}
        await s3.upload_files(**s3_files_data)
        self.logger.debug("{} files uploaded to s3", len(s3_files_data))

        db_files_data = {id: file.filename for id, file in files_data.items()}
        folder = await self.repository.create_folder(lifetime_minutes, db_files_data)
        self.logger.debug("Created Folder(id={})", folder.id)

        return folder

    async def get_folder(self, folder_id: UUID) -> Folder:
        folder = await self.repository.read_folder(folder_id, include_files=True)
        if folder is None:
            self.logger.debug("not found Folder(id={})", folder_id)
            raise FolderNotFound(folder_id)
        if folder.expire_at < datetime.now(UTC):
            raise FolderExpired(folder_id)
        return folder

    async def download_file(self, file_id: UUID) -> StreamingResponse:
        file = await self.repository.read_file(file_id, include_folder=True)
        if file is None:
            raise FileNotFound(file_id)
        if file.folder.expire_at < datetime.now(UTC):
            raise FolderExpired(file.folder.id)

        content, size = await s3.download_file(str(file.id))
        self.logger.debug("Streaming file '{}' from s3", file_id)

        headers = {"Content-Length": str(size)}
        if file.filename:
            headers["Content-Disposition"] = f"attachment; filename={file.filename}"
        return StreamingResponse(content=content, headers=headers)
