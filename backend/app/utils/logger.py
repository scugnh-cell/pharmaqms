import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING

from .const import LOG_DIR

FORMAT_STR = "[%(asctime)s][%(levelname)s]%(message)s"
FORMATTER = logging.Formatter(FORMAT_STR)

DEFAULT_OPTIONS = {
    "maxBytes": 100 * 1024 * 1024,
    "backupCount": 5,
    "encoding": "utf8",
}

RESERVED_LOGGERS = {
    "default": "default.log",
}
LOGGERS = {}
LOG_FUNCS = frozenset(["info", "debug", "warn", "warning", "error", "exception"])

if TYPE_CHECKING:
    def info(msg: str, *args, **kwargs): ...
    def debug(msg: str, *args, **kwargs): ...
    def warn(msg: str, *args, **kwargs): ...
    def warning(msg: str, *args, **kwargs): ...
    def error(msg: str, *args, **kwargs): ...
    def exception(e: Exception, msg: str, *args, **kwargs): ...


def __getattr__(name):
    if name in LOG_FUNCS:
        return getattr(LOGGERS["default"], name)
    if name in LOGGERS:
        return LOGGERS[name]
    raise AttributeError(f"No logger named: {name}")


def init_logger():
    for name, filename in RESERVED_LOGGERS.items():
        LOGGERS[name] = AppLogger(name, filename, **DEFAULT_OPTIONS)


class AppLogger:
    def __init__(self, logger_name, filename, **options):
        log_file_path = os.path.join(LOG_DIR, filename)
        self.filename = filename
        handler = RotatingFileHandler(log_file_path, **options)
        handler.setFormatter(FORMATTER)
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def debug(self, *msg):
        self.logger.debug(self._join(msg))

    def info(self, *msg, **kwargs):
        self.logger.info(self._join(msg))

    def warn(self, *msg):
        self.logger.warning(self._join(msg))

    def warning(self, *msg):
        self.logger.warning(self._join(msg))

    def error(self, *msg):
        self.logger.error(self._join(msg))

    def exception(self, e, *msg):
        import traceback
        error_details = traceback.format_exc()
        full_msg = self._join((*msg, error_details))
        self.logger.error(full_msg)

    def _join(self, args):
        try:
            return "\t".join(str(a) for a in args)
        except Exception:
            return str(args)
