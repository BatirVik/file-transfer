from uuid import uuid4
from typing import BinaryIO, Iterable

from fastapi import UploadFile

from app.aws.s3 import upload_folder
from app.exceptions.files import MissingFilename
from app.repositories.folder import FolderRepository
from app.models.files import Folder

from .base import BaseService


class FolderService(BaseService[FolderRepository]):
    repository_cls = FolderRepository

    async def create_folder(self, files: Iterable[UploadFile]) -> Folder:
        files_kwargs: dict[str, BinaryIO] = {}
        for file in files:
            if file.filename is None:
                self.logger.debug("Some of files have no name")
                raise MissingFilename
            files_kwargs[file.filename] = file.file
        folder_id = uuid4()

        filenames = files_kwargs.keys()
        await upload_folder(str(folder_id), **files_kwargs)
        self.logger.debug("Files uploaded to aws: {}", filenames)

        folder = await self.repository.create_folder(filenames, folder_id)
        self.logger.debug("Created Folder(id={})", folder_id)
        return folder
