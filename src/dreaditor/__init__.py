from __future__ import annotations

import logging
import os
from pathlib import Path

import importlib_metadata

VERSION_STRING = importlib_metadata.version("dreaditor")


def get_appdata_folder() -> Path:
    appdata = Path(os.getenv("APPDATA"))
    folder = appdata.joinpath("Dreaditor")

    if not Path.exists(folder):
        os.mkdir(folder)
    return folder


def get_log_folder() -> Path:
    appdata = get_appdata_folder()
    logFolder = appdata.joinpath("Logs")

    if not Path.exists(logFolder):
        os.mkdir(logFolder)

    return logFolder


def get_data_path() -> Path:
    return Path(__file__).parent.joinpath("data")


def get_stylesheet(sheet_name: str) -> str:
    file = get_data_path().joinpath("qt-stylesheets", sheet_name)

    if not file.exists():
        logging.getLogger(__name__).error("Missing stylesheet: %s", file)
        return ""

    return file.read_text()


def setup_logging(default_level: str, file_level: str, log_to_file: Path | None, quiet: bool = False):
    import logging.config
    import logging.handlers
    import time

    handlers: dict = {
        "default": {
            "level": default_level,
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    }

    if log_to_file is not None:
        handlers["local_app_data"] = {
            "level": file_level,
            "formatter": "default",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": log_to_file,
            "encoding": "utf-8",
            "backupCount": 5,
        }

    logging.Formatter.converter = time.gmtime
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] [%(levelname)s] [%(name)s] %(funcName)s: %(message)s",
                }
            },
            "handlers": handlers,
            "loggers": {},
            "root": {
                "level": "DEBUG",
                "handlers": list(handlers.keys()),
            },
        }
    )
