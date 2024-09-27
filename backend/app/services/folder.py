from collections.abc import Iterable
from uuid import uuid4, UUID
from typing import BinaryIO

from fastapi import UploadFile

from app.aws.s3 import upload_folder
from app.exceptions.files import FilenameMissing, FilenameDuplication, FolderNotFound
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
        await upload_folder(str(folder_id), **files_kwargs)
        self.logger.debug("Files uploaded to aws: {}", filenames)

        folder = await self.repository.create_folder(
            filenames, lifetime_minutes, folder_id
        )
        self.logger.debug("Created Folder(id={})", folder_id)
        return folder

    async def get_folder(self, folder_id: UUID) -> Folder:
        folder = await self.repository.get_folder(folder_id, files_include=True)
        if folder is None:
            self.logger.debug("not found Folder(id={})", folder_id)
            raise FolderNotFound(folder_id)
        return folder
