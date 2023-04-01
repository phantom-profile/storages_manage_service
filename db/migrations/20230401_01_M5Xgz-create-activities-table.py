"""
Create Activities database
"""

from yoyo import step

__depends__ = {}

up = """
    CREATE TABLE activities (
        id INTEGER PRIMARY KEY,
        title STRING NOT NULL,
        start_time DATETIME NOT NULL
    );
"""

down = "DROP TABLE activities;"

steps = [
    step(up, down)
]
