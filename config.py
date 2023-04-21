from os import path
from pathlib import Path
from sqlite3 import Connection

ROOT_DIR = path.dirname(path.abspath(__file__))
DB_PATH = Path(ROOT_DIR) / 'activities_service_db.sqlite3'

DB = Connection(DB_PATH).cursor()
