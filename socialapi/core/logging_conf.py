import logging
from logging.config import dictConfig

from socialapi.core.config import DevConfig, ProdConfig, config


def obfuscate_email(email: str, visible_length: int) -> str:
    visible_chars = email[:visible_length]  # slice of the string
    head, tail = email.split("@")
    return visible_chars + ("*" * (len(head) - visible_length)) + "@" + tail


# Custom Filter
class PIIObfuscatorFilter(logging.Filter):
    def __init__(self, name: str = "", visible_length: int = 2) -> None:
        super().__init__(name)
        self.visible_length = visible_length

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscate_email(record.email, self.visible_length)
        return True


class ExtraInfoFilter(logging.Filter):
    def __init__(self, name: str = "", default_value: str = "-") -> None:
        super().__init__(name)
        self.default_value = default_value

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "received_data"):
            record.received_data = self.default_value
        return True


handlers = ["default", "timed_rotating_file"]
if isinstance(config, ProdConfig):
    handlers.append("logtail")


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
                    "default_value": "-",
                },
                "pii_obfuscation": {
                    "()": PIIObfuscatorFilter,
                    "visible_length": 2 if isinstance(config, DevConfig) else 0,
                },
                "extra_data": {"()": ExtraInfoFilter},
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "[%(correlation_id)s] | %(name)s(%(funcName)s):%(lineno)d - %(message)s - %(received_data)s",
                },
                "file": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | [%(correlation_id)s] | %(name)s(%(funcName)s):%(lineno)d - %(message)s - ",
                },
                "json": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s %(msecs)03d %(levelname)-8s %(correlation_id)s %(name)s %(funcName)s %(lineno)d %(message)s %(received_data)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "pii_obfuscation", "extra_data"],
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
                    "filters": ["correlation_id", "pii_obfuscation", "extra_data"],
                },
                "logtail": {
                    "class": "logtail.LogtailHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "pii_obfuscation", "extra_data"],
                    "source_token": config.LOGTAIL_API_KEY,
                    "host": config.LOGTAIL_HOST,
                },
            },
            "loggers": {
                "socialapi": {
                    "handlers": handlers,
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": handlers,
                    "level": "INFO",
                },
                "databases": {
                    "handlers": handlers,
                    "level": "WARNING",
                },
                "aiosqlite": {
                    "handlers": handlers,
                    "level": "WARNING",
                },
            },
        }
    )
