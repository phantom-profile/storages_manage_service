from os import path
from pathlib import Path
from sqlite3 import Connection


def __dict_factory(cursor, row):
    d = {}
    for idx, column in enumerate(cursor.description):
        d[column[0]] = row[idx]
    return d


def __create_connection():
    db_path = Path(ROOT_DIR) / 'activities_service_db.sqlite3'
    connection = Connection(db_path, check_same_thread=False)
    connection.row_factory = __dict_factory
    return connection


ROOT_DIR = path.dirname(path.abspath(__file__))
DB = __create_connection()
