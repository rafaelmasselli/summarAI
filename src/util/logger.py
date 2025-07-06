import logging
import os
from typing import Optional


class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"


class Logger:
    def __init__(self, log_file: Optional[str] = None):
        self.logger = logging.getLogger("llm_estudy")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def info(self, message: str):
        print(f"{Colors.BLUE}{'=' * 50}{Colors.RESET}")
        self.logger.info(message)
        print(f"{Colors.BLUE}{'=' * 50}{Colors.RESET}")

    def success(self, message: str):
        print(f"{Colors.GREEN}{'=' * 50}{Colors.RESET}")
        self.logger.info(f"{Colors.GREEN}✓ {message}{Colors.RESET}")
        print(f"{Colors.GREEN}{'=' * 50}{Colors.RESET}")

    def warning(self, message: str):
        print(f"{Colors.YELLOW}{'=' * 50}{Colors.RESET}")
        self.logger.warning(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'=' * 50}{Colors.RESET}")

    def error(self, message: str):
        print(f"{Colors.RED}{'=' * 50}{Colors.RESET}")
        self.logger.error(f"{Colors.RED}✗ {message}{Colors.RESET}")
        print(f"{Colors.RED}{'=' * 50}{Colors.RESET}")

    def debug(self, message: str):
        self.logger.debug(message)


logger = Logger(log_file="logs/llm_estudy.log")
