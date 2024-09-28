from collections.abc import Iterable
from datetime import UTC, datetime
from io import BytesIO
from uuid import uuid4, UUID
from typing import BinaryIO

from fastapi import UploadFile

from app.aws import s3
from app.exceptions.files import (
    FileNotFound,
    FilenameMissing,
    FilenameDuplication,
    FolderExpired,
    FolderNotFound,
)
from app.repositories.folder import FilesRepository
from app.models.files import Folder

from .base import BaseService


class FilesService(BaseService[FilesRepository]):
    repository_cls = FilesRepository

    async def create_folder(
        self, files: Iterable[UploadFile], lifetime_minutes: int
    ) -> Folder:
        files_kwargs: dict[str, BinaryIO] = {}
        for file in files:
            filename = file.filename
            if filename is None:
                self.logger.debug("Some of files have no name")
                raise FilenameMissing
            if filename in files_kwargs:
                self.logger.debug("Some of files have duplication name")
                raise FilenameDuplication(filename)
            files_kwargs[filename] = file.file
        folder_id = uuid4()

        filenames = files_kwargs.keys()
        await s3.upload_folder(str(folder_id), **files_kwargs)
        self.logger.debug("Files uploaded to aws: {}", filenames)

        folder = await self.repository.create_folder(
            filenames, lifetime_minutes, folder_id
        )
        self.logger.debug("Created Folder(id={})", folder_id)
        return folder

    async def get_folder(self, folder_id: UUID) -> Folder:
        folder = await self.repository.read_folder(folder_id, include_files=True)
        if folder is None:
            self.logger.debug("not found Folder(id={})", folder_id)
            raise FolderNotFound(folder_id)

        if folder.expire_at < datetime.now(UTC).replace(tzinfo=None):
            raise FolderExpired(folder_id)
        return folder

    async def download_file(self, folder_id: UUID, filename: str) -> tuple[BytesIO, int]:
        folder = await self.get_folder(folder_id)
        for file in folder.files:
            if file.filename == filename:
                foldername = str(folder_id)
                self.logger.debug(
                    "Start download from aws: {}/{}", foldername, filename
                )
                return await s3.download_file(foldername, filename)
        self.logger.debug("not found File(id={})", folder_id)
        raise FileNotFound(filename)
