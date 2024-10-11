from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.clean import clean_expired
from app.models.files import Folder
from app.aws.s3 import get_s3_resource
from app.config import config


@pytest.mark.asyncio
async def test_clean_expired(
    db: AsyncSession, db_folder: Folder, db_expired_folder: Folder
):
    await clean_expired()

    folder = await db.scalar(
        select(Folder).where(Folder.id == db_folder.id).limit(1),
    )
    assert folder

    folder = await db.scalar(
        select(Folder).where(Folder.id == db_expired_folder.id).limit(1),
    )
    assert folder is None

    remain_files_ids = set()
    async with get_s3_resource() as resource:
        bucket = await resource.Bucket(config.S3_BUCKET_NAME)
        async for obj in bucket.objects.all():
            remain_files_ids.add(UUID(obj.key))

    expected_files_ids = {file.id for file in db_folder.files}
    assert remain_files_ids == expected_files_ids
