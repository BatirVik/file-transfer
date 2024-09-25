from typing import Type
from app.dependencies.database import SessionDepends
from app.repositories.base import BaseRepository
from app.logger import LoggerDepends


class BaseService[T: BaseRepository]:
    repository_cls: Type[T]

    def __init__(self, db: SessionDepends, logger: LoggerDepends) -> None:
        self.db = db
        self.logger = logger
        self.repository = self.repository_cls(db)
