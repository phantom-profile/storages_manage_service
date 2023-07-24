from storages_manage_service.settings import BASE_DIR
from datetime import datetime


class DefaultLogger:
    def __init__(self, log_name: str):
        self.log_path = f"{BASE_DIR}/log/{log_name}"

    def info(self, message: str, extra_params: dict = None):
        log_file = open(self.log_path, "a")
        print(f"[{datetime.now()}] I, {message}, extra params = {extra_params}", file=log_file)
        log_file.close()

    def warn(self, error: Exception, extra_params: dict = None):
        log_file = open(self.log_path, "a")
        if error.args == ():
            print(f"[{datetime.now()}] W, catched error class - {type(error)}, information not provided, extra params = {extra_params}", file=log_file)
        else:
            print(
                f"[{datetime.now()}] W, catched error class - {type(error)}, provided information - {error}, extra params = {extra_params}", file=log_file)
        log_file.close()


s = MemoryError("asd")
a = DefaultLogger("logasdad.log")
a.warn(s)

print(s.args)