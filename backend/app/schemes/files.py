from datetime import datetime
from uuid import UUID
from fastapi import UploadFile
from pydantic import BaseModel, Field, field_validator


class FolderRead(BaseModel):
    id: UUID
    files: list[str]
    expire_at: datetime

    @field_validator("files", mode="before")
    def files_(cls, files: list) -> list[str]:
        try:
            return [file.filename for file in files]
        except Exception:
            return files


class FolderCreate(BaseModel):
    files: list[UploadFile]
    lifetime_minutes: int = Field(
        1440, ge=1, le=20160, alias="lifetimeMinutes"
    )  # default: 1 day, max: 2 weeks
