"""
Logging Utility
Sets up structured, coloured console + rotating file logging.
"""

import logging
import logging.handlers
import os
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

COLORS = {
    "DEBUG": "\033[94m",
    "INFO": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "CRITICAL": "\033[95m",
    "RESET": "\033[0m",
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, COLORS["RESET"])
        reset = COLORS["RESET"]
        record.levelname = f"{color}{record.levelname:<8}{reset}"
        return super().format(record)


def setup_logger(name: str = "api_tests", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # already configured

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Console handler (coloured)
    ch = logging.StreamHandler()
    ch.setFormatter(ColorFormatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    # Rotating file handler
    fh = logging.handlers.RotatingFileHandler(
        LOG_DIR / "test_run.log",
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,
        encoding="utf-8"
    )
    fh.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
