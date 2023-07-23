from storages_manage_service.settings import BASE_DIR
from datetime import datetime


class DefaultLogger:
    def __init__(self, log_name: str):
        self.log_path = f"{BASE_DIR}/log/{log_name}"

    def info(self, message: str):
        log_file = open(self.log_path, "w+")
        log_file.write(f"[{datetime.now()}] I, {message}")
        log_file.close()


a = DefaultLogger("log.log")
a.info("adad")