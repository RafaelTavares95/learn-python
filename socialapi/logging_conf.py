from logging.config import dictConfig

from socialapi.config import DevConfig, config


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                },
                "timed_rotating_file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "logs/socialapi.log",
                    "when": "midnight",
                    "backupCount": 5,
                    "encoding": "utf8",
                    "utc": True,
                },
            },
            "loggers": {
                "socialapi": {
                    "handlers": ["default", "timed_rotating_file"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["default", "timed_rotating_file"],
                    "level": "INFO",
                },
                "databases": {
                    "handlers": ["default", "timed_rotating_file"],
                    "level": "WARNING",
                },
                "aiosqlite": {
                    "handlers": ["default", "timed_rotating_file"],
                    "level": "WARNING",
                },
            },
        }
    )
