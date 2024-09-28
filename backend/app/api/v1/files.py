from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.exceptions.files import (
    FilenameMissing,
    FilenameDuplication,
    FolderExpired,
    FolderNotFound,
    FileNotFound,
)
from app.schemes.files import FolderRead
from app.models.files import Folder
from app.services.folder import FilesService

router = APIRouter(prefix="/files", tags=["files"])


@router.post(
    "/folder",
    status_code=201,
    response_model=FolderRead,
    responses={400: {"description": "Duplicate or missing filename"}},
)
async def upload_files(
    files: list[UploadFile],
    files_service: FilesService = Depends(),
    lifetime_minutes: int = Body(
        default=1440,
        ge=1,
        le=20160,
        alias="lifetimeMinutes",
        description="After the folder expires, the folder and its files will no longer be available",
    ),
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
    folder_id: UUID, files_service: FilesService = Depends()
) -> Folder:
    try:
        return await files_service.get_folder(folder_id)
    except FolderNotFound:
        raise HTTPException(404, "Folder not found")
    except FolderExpired:
        raise HTTPException(410, "Folder is no longer available")


@router.get("/folder/{folder_id}/{filename}")
async def get_file(
    filename: str, folder_id: UUID, files_service: FilesService = Depends()
) -> StreamingResponse:
    try:
        stream, content_length = await files_service.download_file(folder_id, filename)
        return StreamingResponse(
            stream,
            media_type="application/octet-stream",
            headers={"Content-Length": str(content_length)},
        )
    except FolderNotFound:
        raise HTTPException(404, "Folder not found")
    except FileNotFound:
        raise HTTPException(404, "File not found")
    except FolderExpired:
        raise HTTPException(410, "Folder is no longer available")
