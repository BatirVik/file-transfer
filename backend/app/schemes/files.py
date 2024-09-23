from uuid import UUID
from pydantic import BaseModel


class FolderIdRead(BaseModel):
    id: UUID
