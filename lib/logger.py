from storages_manage_service.settings import BASE_DIR
from datetime import datetime
from os import path, mkdir


class WrongLogName(Exception):
    MESSAGE = "The entered file name does not match the format (name.log)"

    def __init__(self):
        super().__init__(self.MESSAGE)


class AppLogger:
    EXTENSION = 'log'
    LOG_DIR = BASE_DIR / "log"

    def __init__(self, filename: str):
        name_as_list = filename.split(".")
        if len(name_as_list) != 2 or name_as_list[-1] != 'log':
            raise WrongLogName()

        self.filename = filename
        self.params = None

    def info(self, message: str, params: dict = None):
        self.params = params
        with open(self.filepath, "a") as log_file:
            print(self._string_template(f"I, {message}"), file=log_file)

    def warn(self, error: Exception, params: dict = None):
        self.params = params
        info = f"info - {error.args}" if error.args else "information not provided"
        with open(self.filepath, "a") as log_file:
            print(self._string_template(f"W, error - {type(error)}, {info}"), file=log_file)

    @property
    def filepath(self):
        if path.exists(self.LOG_DIR):
            return self.LOG_DIR / self.filename
        mkdir(self.LOG_DIR)
        return self.LOG_DIR / self.filename

    def _validate_file_name(self, filename: str):
        name_as_list = filename.split(".")
        if len(name_as_list) != 2 or name_as_list[-1] != self.EXTENSION:
            raise WrongLogName()

    def _string_template(self, inserted: str):
        return f"[{datetime.now()}] {inserted}, extra params = {self.params}"


default_logger = AppLogger("log.log")
