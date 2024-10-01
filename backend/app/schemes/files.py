from datetime import datetime
from uuid import UUID
from fastapi import UploadFile
from pydantic import BaseModel, Field


class FileRead(BaseModel):
    id: UUID
    filename: str | None


class FolderRead(BaseModel):
    id: UUID
    files: list[FileRead]
    expire_at: datetime = Field(serialization_alias="expireAt")


class FolderCreate(BaseModel):
    files: list[UploadFile]
    lifetime_minutes: int = Field(
        1440, ge=1, le=20160, alias="lifetimeMinutes"
    )  # default: 1 day, max: 2 weeks
