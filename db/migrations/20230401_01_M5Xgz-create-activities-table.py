"""
Create Activities table
"""

from yoyo import step

__depends__ = {}

up = """
    CREATE TABLE activities (
        id INTEGER PRIMARY KEY,
        title STRING NOT NULL,
        start_time DATETIME NOT NULL,
        is_done BOOLEAN NOT NULL DEFAULT FALSE,
        description TEXT NOT NULL DEFAULT ""
    );
"""

down = "DROP TABLE activities;"

steps = [
    step(up, down)
]
