from datetime import datetime
import time
import threading
import os
from .file_utils import f_mkdir, f_join, f_abspath


class Logger:
    _instances = {}
    _lock = threading.Lock()

    COLORS = {
        "INFO": "\033[92m",     # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",    # Red
        "DEBUG": "\033[94m",    # Blue
        "ENDC": "\033[0m",      # Reset
    }

    def __new__(
            cls, 
            process_name: str, 
            project_root: str, 
            base_dir: str = "logs"
        ):
        with cls._lock:
            if process_name not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[process_name] = instance
            return cls._instances[process_name]

    def __init__(
            self, 
            process_name: str, 
            project_root: str, 
            base_dir: str = "logs"
        ):
        self._process_name = process_name
        start_time = time.strftime("%Y%m%d_%H%M%S")
        log_path = f_join(project_root, base_dir, process_name, f"{process_name}_{start_time}.log")
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.log_path = log_path
        f_mkdir(os.path.dirname(self.log_path))
        self._initialized = True

    def _write(self, message: str):
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def _format(self, message: str, level: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{self._process_name} - [{timestamp}] - [{level}]: {message}"
    
    def _color(self, text: str, level: str) -> str:
        color = self.COLORS.get(level, "")
        endc = self.COLORS["ENDC"]
        return f"{color}{text}{endc}"

    def log(self, message: str, level: str = "INFO") -> None:
        formatted = self._format(message, level)
        self._write(formatted)
        print(self._color(formatted, level))

    def info(self, message: str) -> None:
        self.log(message, "INFO")

    def warning(self, message: str) -> None:
        self.log(message, "WARNING")

    def error(self, message: str) -> None:
        self.log(message, "ERROR")

    def debug(self, message: str):
        self.log(message, "DEBUG")