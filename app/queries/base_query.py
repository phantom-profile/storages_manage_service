from typing import Protocol

from app.main import db


class AbstractQuery(Protocol):
    def get_sql(self) -> str: ...


class BaseQuery:
    TABLE = None

    def execute(self) -> list:
        return list(db.execute(self._build().get_sql()))

    def _build(self) -> AbstractQuery:
        raise NotImplementedError('build query in subclass')
