from sqlalchemy.ext.asyncio.session import AsyncSession


class BaseRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
