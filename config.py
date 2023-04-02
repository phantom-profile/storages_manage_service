from os import path
from pathlib import Path

ROOT_DIR = path.dirname(path.abspath(__file__))
DB_PATH = Path(ROOT_DIR) / 'activities_service_db.sqlite3'
