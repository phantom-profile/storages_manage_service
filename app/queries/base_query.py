import sqlite3
from typing import Protocol

from config import DB


class AbstractQuery(Protocol):
    def get_sql(self) -> str: ...


class BaseQuery:
    TABLE = None

    def __init__(self):
        self.__connection = DB.cursor()
        self.__query = None
        self.result = None
        self.is_successful = None
        self.error_message = ''

    def execute(self):
        try:
            self.__connection.execute(self.query)
            print(self.query)
            if self.__is_insert():
                DB.commit()
            else:
                self.result = self.__connection.fetchall()
            self.is_successful = True
        except sqlite3.Error as e:
            self.is_successful = False
            self.error_message = str(e)
        finally:
            self.__connection.close()

    @property
    def query(self) -> str:
        if not self.__query:
            self.__query = self._build().get_sql()

        return self.__query

    def __is_insert(self) -> bool:
        return self.query.startswith('INSERT')

    def _build(self) -> AbstractQuery:
        raise NotImplementedError('build query in subclass')
