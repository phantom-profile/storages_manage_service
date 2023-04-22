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
        self.error_message = ''

    def execute(self):
        try:
            self.__connection.execute(self.query)
            print(self.query)
            if not self.__is_select():
                DB.commit()
            else:
                self.result = self.__connection.fetchall()
        except sqlite3.Error as e:
            self.error_message = str(e)
        finally:
            self.__connection.close()

    @property
    def is_successful(self) -> bool:
        return self.error_message == ''

    @property
    def query(self) -> str:
        if not self.__query:
            self.__query = self._build().get_sql()

        return self.__query

    def __is_select(self) -> bool:
        return self.query.startswith('SELECT')

    def _build(self) -> AbstractQuery:
        raise NotImplementedError('build query in subclass')
