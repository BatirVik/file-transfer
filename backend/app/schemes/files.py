from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class FileRead(BaseModel):
    id: UUID
    filename: str | None


class FolderRead(BaseModel):
    id: UUID
    files: list[FileRead]
    expire_at: datetime = Field(serialization_alias="expireAt")
