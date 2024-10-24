from collections.abc import Iterable
from datetime import UTC, datetime
from typing import AsyncIterable, NamedTuple
from uuid import uuid4, UUID

from fastapi import UploadFile

from app.aws import s3
from app.repositories.files import FilesRepository
from app.models.files import Folder, File
from app.exceptions.files import (
    FileNotFound,
    FolderExpired,
    FolderNotFound,
)

from .base import BaseService


class DownloadResp(NamedTuple):
    stream: AsyncIterable[bytes]
    length: int | None = None
    filename: str | None = None


class FilesService(BaseService[FilesRepository]):
    repository_cls = FilesRepository

    async def create_folder(
        self, files: Iterable[UploadFile], lifetime_minutes: int
    ) -> Folder:
        files_data = {uuid4(): file for file in files}

        s3_files_data = {str(id): file.file for id, file in files_data.items()}
        await s3.upload_files(**s3_files_data)

        self.logger.debug("{} files uploaded to s3", len(s3_files_data))

        folder = await self.repository.create_folder(lifetime_minutes, files_data)
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

    async def get_file(self, file_id: UUID) -> File:
        file = await self.repository.read_file(file_id, include_folder=True)
        if file is None:
            raise FileNotFound(file_id)
        if file.folder.expire_at < datetime.now(UTC):
            raise FolderExpired(file.folder.id)
        return file

    async def download_file(self, file_id: UUID) -> DownloadResp:
        file = await self.get_file(file_id)
        stream, length = await s3.download_file(str(file.id))
        self.logger.debug("Streaming file '{}' from s3", file.id)
        filename = file.filename or str(file.id)
        return DownloadResp(stream=stream, length=length, filename=filename)

    async def download_folder(self, folder_id: UUID) -> DownloadResp:
        folder = await self.get_folder(folder_id)
        filenames = {
            str(file.id): file.filename or str(file.id) for file in folder.files
        }
        stream = s3.download_files_zip(filenames)
        self.logger.debug("Streaming folder '{}' files into zip from s3", folder.id)
        return DownloadResp(stream=stream, filename=f"{folder.id}.zip")
