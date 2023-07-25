from storages_manage_service.settings import BASE_DIR
from datetime import datetime


class WrongLogName(Exception):
    """The entered file name does not match the format (name.log)"""


class DefaultLogger:
    def __init__(self, log_name: str):
        if not self.__correct_log_file_name(log_name):
            raise WrongLogName("The entered file name does not match the format (name.log)")
        self.log_path = BASE_DIR / "log" / log_name

    def info(self, message: str, extra_params: dict = None):
        with open(self.log_path, "a") as log_file:
            print(self.__build_log_str(message=message, extra_params=extra_params), file=log_file)

    def warn(self, error: Exception, extra_params: dict = None):
        with open(self.log_path, "a") as log_file:
            print(self.__build_log_str(error=error, extra_params=extra_params), file=log_file)

    @staticmethod
    def __correct_log_file_name(name: str):
        split_string = name.split(".")
        if len(split_string) == 2 and split_string[-1] == "log":
            return True

    @staticmethod
    def __build_log_str(message: str = None, error: Exception = None, extra_params: dict = None) -> str:
        if message:
            return f"[{datetime.now()}] I, {message}, extra params = {extra_params}"
        if not error.args:
            return f"[{datetime.now()}] W, catched error class - {type(error)}, information not provided, extra " \
                   f"params = {extra_params}"
        return f"[{datetime.now()}] W, catched error class - {type(error)}, info - {error.args}, extra " \
               f"params = {extra_params}"
