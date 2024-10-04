from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, uuidpk


class File(Base):
    __tablename__ = "file"

    id: Mapped[uuidpk]
    filename: Mapped[str | None]
    size: Mapped[int | None]
    folder_id: Mapped[UUID] = mapped_column(ForeignKey("folder.id"))

    folder: Mapped["Folder"] = relationship(back_populates="files")


class Folder(Base):
    __tablename__ = "folder"

    id: Mapped[uuidpk]
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    files: Mapped[list["File"]] = relationship(
        back_populates="folder", cascade="all, delete-orphan"
    )
