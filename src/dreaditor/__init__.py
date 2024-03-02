import os
import logging

from pathlib import Path


VERSION_STRING = "0.1.0"

def get_appdata_folder() -> Path:
    appdata = Path(os.getenv('APPDATA'))
    print(appdata)
    folder = appdata.joinpath("Dreaditor")

    if not Path.exists(appdata):
        os.mkdir(appdata)
    
    return appdata

def get_log_folder() -> Path:
    appdata = get_appdata_folder()
    logFolder = appdata.joinpath("Logs")

    if not Path.exists(logFolder):
        os.mkdir(logFolder)

    return logFolder

def get_config_file_path() -> Path:
    return get_appdata_folder().joinpath("config.json")


def get_data_path() -> Path:
    return Path(__file__).parent.joinpath("data")

def get_stylesheet(sheet_name: str) -> str:
    file = get_data_path().joinpath("qt-stylesheets", sheet_name)
    
    if not file.exists():
        logging.log(3, f"Stylesheet {sheet_name} does not exist!")
        return ""
    
    return file.read_text()

def setup_logging(default_level: str,  log_to_file: Path | None, quiet: bool = False):
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
            "level": "DEBUG",
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
            "loggers": {
            },
            "root": {
                "level": default_level,
                "handlers": list(handlers.keys()),
            },
        }
    )