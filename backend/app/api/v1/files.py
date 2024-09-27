from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Depends, UploadFile

from app.services.folder import FilesService
from app.exceptions.files import FilenameMissing, FilenameDuplication, FolderNotFound
from app.schemes.files import FolderRead
from app.models.files import Folder

router = APIRouter(prefix="/files", tags=["files"])


@router.post(
    "/folder",
    status_code=201,
    response_model=FolderRead,
    responses={400: {"description": "Duplicate or missing filename"}},
)
async def upload_files(
    files_service: Annotated[FilesService, Depends()],
    files: list[UploadFile],
    lifetime_minutes: Annotated[
        int, Body(ge=1, le=20160, alias="lifetimeMinutes")
    ] = 1440,
) -> Folder:
    try:
        return await files_service.create_folder(files, lifetime_minutes)
    except FilenameMissing:
        raise HTTPException(400, "All files must have a filename")
    except FilenameDuplication:
        raise HTTPException(400, "All files must have a unique filename")


@router.get(
    "/folder/{folder_id}",
    response_model=FolderRead,
    responses={404: {"description": "Folder not found"}},
)
async def get_folder(
    files_service: Annotated[FilesService, Depends()], folder_id: UUID
) -> Folder:
    try:
        return await files_service.get_folder(folder_id)
    except FolderNotFound:
        raise HTTPException(404, "Folder not found")
