from colorama import Fore, Style, init
from coloredlogs import ColoredFormatter
from src.config import settings

init(convert=settings.logging.cmd_convert_revert)

LEVEL = "DEBUG" if settings.logging.debug else "INFO"

file_format = "%(asctime)s | %(levelname)-8s| %(name)s | %(lineno)d - %(message)s"

dictLogConfig = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": ColoredFormatter,
            "fmt": file_format,
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "%",
            "level_styles": {
                "debug": {"color": "white"},
                "info": {"color": "cyan"},
                "warning": {"color": "yellow"},
                "error": {"color": "red"},
                "critical": {"color": "red", "bold": True},
            },
            "field_styles": {
                "asctime": {"color": "white"},
                "name": {"color": "blue"},
                "lineno": {"color": "blue"},
            },
        },
        "file_format": {
            "format": file_format,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LEVEL,
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "file_format",
            "filename": "src/logs/logs.log",
            "encoding": "utf8",
            "maxBytes": 1 * 1024 * 1024,
            "backupCount": 3
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "file_format",
            "filename": "src/logs/error_logs.log",
            "encoding": "utf8",
            "maxBytes": 1 * 1024 * 1024,
            "backupCount": 3
        },
    },
    "root": {
        "level": LEVEL,
        "handlers": ["console", "file", "error_file"],
    },
}
