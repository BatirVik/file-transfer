from typing import Type
from app.dependencies.database import SessionDepends
from app.repositories.base import BaseRepository


class BaseService:
    repository_cls: Type[BaseRepository]

    def __init__(self, db: SessionDepends) -> None:
        self.db = db
        self.repository = getattr(type(self), "repository_cls")(db)
