from storages_manage_service.settings import BASE_DIR
from datetime import datetime
from os import path, mkdir


class WrongLogName(Exception):
    ...


class AppLogger:
    NAME_ERROR = "The entered file name does not match the format (name.log)"
    LOG_DIR = BASE_DIR / "log"

    def __init__(self, filename: str):
        name_as_list = filename.split(".")
        if len(name_as_list) != 2 or name_as_list[-1] != 'log':
            raise WrongLogName(self.NAME_ERROR)

        self.filename = filename
        self.params = None

    def info(self, message: str, params: dict = None):
        self.params = params
        with open(self.filepath, "a") as log_file:
            print(self._mklog(f"I, {message}"), file=log_file)

    def warn(self, error: Exception, params: dict = None):
        self.params = params
        with open(self.filepath, "a") as log_file:
            print(self._mklog(f"W, error - {type(error)}, info - {error.args}"), file=log_file)

    @property
    def filepath(self):
        if path.exists(self.LOG_DIR):
            return self.LOG_DIR / self.filename
        mkdir(self.LOG_DIR)
        return self.LOG_DIR / self.filename

    def _mklog(self, inserted: str):
        return f"[{datetime.now()}] {inserted}, extra params = {self.params or {}}"


default_logger = AppLogger("log.log")
