from typing import Protocol, Iterable

from config import DB


class AbstractQuery(Protocol):
    def get_sql(self) -> str: ...


class BaseQuery:
    TABLE = None

    def execute(self) -> Iterable:
        return DB.execute(self._build().get_sql())

    def _build(self) -> AbstractQuery:
        raise NotImplementedError('build query in subclass')
