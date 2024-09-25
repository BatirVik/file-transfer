from datetime import datetime
from uuid import UUID
from fastapi import UploadFile, File
from pydantic import BaseModel, Field


class FolderRead(BaseModel):
    id: UUID
    expire_at: datetime


class FolderCreate(BaseModel):
    files: list[UploadFile]
    lifetime_minutes: int = Field(
        1440, ge=1, le=20160, alias="lifetimeMinutes"
    )  # default: 1 day, max: 2 weeks
