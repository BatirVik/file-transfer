from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class FileRead(BaseModel):
    id: UUID
    folder_id: UUID = Field(serialization_alias="folderId")
    filename: str | None
    size: int | None


class FolderFileRead(BaseModel):
    id: UUID
    filename: str | None
    size: int | None


class FolderRead(BaseModel):
    id: UUID
    files: list[FolderFileRead]
    expire_at: datetime = Field(serialization_alias="expireAt")
