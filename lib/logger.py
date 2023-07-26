from storages_manage_service.settings import BASE_DIR
from datetime import datetime
from os import path, mkdir


class WrongLogName(Exception):
    """The entered file name does not match the format (name.log)"""


class AppLogger:
    LOG_DIR = BASE_DIR / "log"

    def __init__(self, log_name: str):
        self.__correct_log_file_name(log_name)
        self.log_path = self.__create_path(log_name)

    def info(self, message: str, extra_params: dict = None):
        with open(self.log_path, "a") as log_file:
            print(self.__build_log_str(message=message, extra_params=extra_params), file=log_file)

    def warn(self, error: Exception, extra_params: dict = None):
        with open(self.log_path, "a") as log_file:
            print(self.__build_log_str(error=error, extra_params=extra_params), file=log_file)

    @staticmethod
    def __correct_log_file_name(name: str):
        if len(name.split(".")) != 2 or name.split(".")[-1] != "log":
            raise WrongLogName("The entered file name does not match the format (name.log)")

    @staticmethod
    def __build_log_str(message: str = None, error: Exception = None, extra_params: dict = None) -> str:
        if message:
            return f"[{datetime.now()}] I, {message}, extra params = {extra_params}"
        if not error.args:
            info = "information not provided"
        else:
            info = f"info - {error.args}"
        return f"[{datetime.now()}] W, catched error class - {type(error)}, {info}, extra params = {extra_params}"

    def __create_path(self, name: str):
        if path.exists(self.LOG_DIR):
            return self.LOG_DIR / name
        mkdir(self.LOG_DIR)
        return self.LOG_DIR / name
