from typing import Annotated
from fastapi import APIRouter, HTTPException, UploadFile, Depends

from app.services.folder import FolderService
from app.models.files import Folder
from app.exceptions.files import MissingFilename
from app.schemes.files import FolderIdRead


router = APIRouter(prefix="/files", tags=["files"])


@router.post("/folder", status_code=201, response_model=FolderIdRead)
async def upload_files(
    folder_service: Annotated[FolderService, Depends()],
    files: list[UploadFile],
) -> Folder:
    try:
        return await folder_service.create_folder(files)
    except MissingFilename:
        raise HTTPException(400, "All files must have a filename")
