from uuid import uuid4
from loguru import logger
from typing import BinaryIO, Iterable

from fastapi import UploadFile

from app.s3 import upload_folder
from app.exceptions.files import MissingFilename
from app.repositories.folder import FolderRepository
from app.models.files import Folder

from .base import BaseService


class FolderService(BaseService):
    repository_cls = FolderRepository
    repository: FolderRepository

    async def create_folder(self, files: Iterable[UploadFile]) -> Folder:
        files_kwargs: dict[str, BinaryIO] = {}
        for file in files:
            if file.filename is None:
                raise MissingFilename
            files_kwargs[file.filename] = file.file
        folder_id = uuid4()
        filenames = files_kwargs.keys()
        await upload_folder(str(folder_id), **files_kwargs)
        return await self.repository.create_folder(filenames, folder_id)
