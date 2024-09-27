from datetime import datetime
from uuid import UUID
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.schema import ForeignKey

from .base import Base, uuidpk


class File(Base):
    __tablename__ = "file"

    id: Mapped[uuidpk]
    filename: Mapped[str]
    folder_id: Mapped[UUID] = mapped_column(ForeignKey("folder.id"))

    folder: Mapped["Folder"] = relationship(back_populates="files")

    __table_args__ = (
        UniqueConstraint("filename", "folder_id", name="uq_filename_folder_id"),
    )


class Folder(Base):
    __tablename__ = "folder"

    id: Mapped[uuidpk]
    expire_at: Mapped[datetime]

    files: Mapped[list["File"]] = relationship(
        back_populates="folder", cascade="all, delete-orphan"
    )
