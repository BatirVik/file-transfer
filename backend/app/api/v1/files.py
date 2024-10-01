from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.exceptions.files import (
    FolderExpired,
    FolderNotFound,
    FileNotFound,
)
from app.schemes.files import FolderRead
from app.models.files import Folder
from app.services.files import FilesService

router = APIRouter(tags=["files"])


@router.get(
    "/files/{file_id}",
    responses={
        404: {"description": "Not Found"},
        410: {"description": "Expired"},
    },
)
async def get_file(
    file_id: UUID, files_service: FilesService = Depends()
) -> StreamingResponse:
    try:
        return await files_service.download_file(file_id)
    except FileNotFound:
        raise HTTPException(404, "File not found")
    except FolderExpired:
        raise HTTPException(410, "File is no longer available")


@router.post("/folders", status_code=201, response_model=FolderRead)
async def upload_files(
    files: list[UploadFile],
    lifetime_minutes: int = Body(
        default=1440,
        ge=1,
        le=20160,
        validation_alias="lifetimeMinutes",
        description="After the folder expires, the folder and its files will no longer be available",
    ),
    files_service: FilesService = Depends(),
) -> Folder:
    return await files_service.create_folder(files, lifetime_minutes)


@router.get(
    "/folders/{folder_id}",
    response_model=FolderRead,
    responses={
        404: {"description": "Not Found"},
        410: {"description": "Expired"},
    },
)
async def get_folder(
    folder_id: UUID, files_service: FilesService = Depends()
) -> Folder:
    try:
        return await files_service.get_folder(folder_id)
    except FolderNotFound:
        raise HTTPException(404, "Folder not found")
    except FolderExpired:
        raise HTTPException(410, "Folder is no longer available")
