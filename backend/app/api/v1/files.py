from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Depends, UploadFile

from app.services.folder import FolderService
from app.models.files import Folder
from app.exceptions.files import FilenameMissing, FilenameDuplication
from app.schemes.files import FolderRead


router = APIRouter(prefix="/files", tags=["files"])


@router.post("/folder", status_code=201, response_model=FolderRead)
async def upload_files(
    folder_service: Annotated[FolderService, Depends()],
    files: list[UploadFile],
    lifetime_minutes: Annotated[
        int, Body(ge=1, le=20160, alias="lifetimeMinutes")
    ] = 1440,
) -> Folder:
    try:
        return await folder_service.create_folder(files, lifetime_minutes)
    except FilenameMissing:
        raise HTTPException(400, "All files must have a filename")
    except FilenameDuplication:
        raise HTTPException(400, "All files must have a unique filename")
