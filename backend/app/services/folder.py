from collections.abc import Iterable
from uuid import uuid4
from typing import BinaryIO

from fastapi import UploadFile

from app.aws.s3 import upload_folder
from app.exceptions.files import FilenameMissing, FilenameDuplication
from app.repositories.folder import FolderRepository
from app.models.files import Folder

from .base import BaseService


class FolderService(BaseService[FolderRepository]):
    repository_cls = FolderRepository

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
