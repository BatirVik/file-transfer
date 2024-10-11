from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from app.models.files import File, Folder
from app.database import session_factory
from app.aws import s3


async def clear_expired() -> None:
    stmt = select(File.id).join(Folder).where(Folder.expire_at < datetime.now(UTC))
    async with session_factory() as db:
        files_ids = await db.scalars(stmt)

    s3_filenames = (str(id) for id in files_ids)
    exceptions = await s3.delete_files(s3_filenames)

    files_to_delete: list[UUID] = []
    for s3_filename, exception in exceptions.items():
        if exception is None:
            files_to_delete.append(UUID(s3_filename))
        else:
            logger.error(
                "Failed to remove an expired file from aws: {!r}",
                exception,
            )

    async with session_factory() as db:
        for file_id in files_to_delete:
            stmt = delete(File).where(File.id == file_id)
            try:
                await db.execute(stmt)
                await db.commit()
            except SQLAlchemyError as exception:
                logger.error(
                    "Failed to remove metadata of an expired file from database: {!r}",
                    exception,
                )
                await db.rollback()

        # remove empty folders
        subquery = select(File.folder_id).group_by(File.folder_id)
        stmt = delete(Folder).where(Folder.id.not_in(subquery))
        await db.execute(stmt)
        await db.commit()
