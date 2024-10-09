from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.schemes.files import FileRead, FolderRead
from app.models.files import Folder, File
from app.services.files import FilesService
from app.exceptions.files import (
    FolderExpired,
    FolderNotFound,
    FileNotFound,
)

router = APIRouter(tags=["files"])


@router.get(
    "/files/{file_id}/download",
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "Successful Response",
            "content": {"applicatation/octet-stream": {}},
        },
        404: {"description": "Not Found"},
        410: {"description": "Expired"},
    },
)
async def get_file_content(
    file_id: UUID, files_service: FilesService = Depends()
) -> StreamingResponse:
    try:
        resp = await files_service.download_file(file_id)
    except FileNotFound:
        raise HTTPException(404, "File not found")
    except FolderExpired:
        raise HTTPException(410, "File is no longer available")

    headers = {}
    if resp.length is not None:
        headers["Content-Length"] = str(resp.length)
    if resp.filename is not None:
        headers["Content-Disposition"] = f'attachment; filename="{resp.filename}"'
    return StreamingResponse(
        content=resp.stream, headers=headers, media_type="application/octet-stream"
    )


@router.get(
    "/files/{file_id}",
    response_model=FileRead,
    responses={
        404: {"description": "Not Found"},
        410: {"description": "Expired"},
    },
)
async def get_file_info(file_id: UUID, files_service: FilesService = Depends()) -> File:
    try:
        return await files_service.get_file(file_id)
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
async def get_folder_info(
    folder_id: UUID, files_service: FilesService = Depends()
) -> Folder:
    try:
        return await files_service.get_folder(folder_id)
    except FolderNotFound:
        raise HTTPException(404, "Folder not found")
    except FolderExpired:
        raise HTTPException(410, "Folder is no longer available")


@router.get(
    "/folders/{folder_id}/download",
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "Successful Response",
            "content": {"applicatation/octet-stream": {}},
        },
        404: {"description": "Not Found"},
        410: {"description": "Expired"},
    },
)
async def get_folder_zip(
    folder_id: UUID, files_service: FilesService = Depends()
) -> StreamingResponse:
    try:
        resp = await files_service.download_folder(folder_id)
    except FolderNotFound:
        raise HTTPException(404, "Folder not found")
    except FolderExpired:
        raise HTTPException(410, "Folder is no longer available")

    headers = {}
    if resp.length is not None:
        headers["Content-Length"] = str(resp.length)
    if resp.filename is not None:
        headers["Content-Disposition"] = f'attachment; filename="{resp.filename}"'
    return StreamingResponse(
        content=resp.stream, headers=headers, media_type="application/zip"
    )
