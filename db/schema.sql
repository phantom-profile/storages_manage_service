CREATE TABLE IF NOT EXISTS "yoyo_lock" (locked INT DEFAULT 1, ctime TIMESTAMP,pid INT NOT NULL,PRIMARY KEY (locked));
CREATE TABLE IF NOT EXISTS "_yoyo_log" ( id VARCHAR(36), migration_hash VARCHAR(64), migration_id VARCHAR(255), operation VARCHAR(10), username VARCHAR(255), hostname VARCHAR(255), comment VARCHAR(255), created_at_utc TIMESTAMP, PRIMARY KEY (id));
CREATE TABLE IF NOT EXISTS "_yoyo_version" (version INT NOT NULL PRIMARY KEY, installed_at_utc TIMESTAMP);
CREATE TABLE IF NOT EXISTS "_yoyo_migration" ( migration_hash VARCHAR(64), migration_id VARCHAR(255), applied_at_utc TIMESTAMP, PRIMARY KEY (migration_hash));
CREATE TABLE activities (
        id INTEGER PRIMARY KEY,
        title STRING NOT NULL,
        start_time DATETIME NOT NULL,
        is_done BOOLEAN NOT NULL DEFAULT FALSE,
        description TEXT NOT NULL DEFAULT ""
    );
