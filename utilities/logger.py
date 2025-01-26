import logging
import os

import coloredlogs


class Logger:
    _instance = None
    default_log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

    @classmethod
    def get_instance(cls, log_level=None):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.logger = logging.getLogger("reporting_global_logger")
            if log_level is None:
                log_level = cls.default_log_level
            cls._instance.configure_logger(log_level)
        return cls._instance

    def configure_logger(self, level):
        level_styles = {
            'debug': {'color': 'white', 'faint': True},
            'info': {'color': 'blue', 'bold': True},
            'warning': {'color': 'yellow'},
            'error': {'color': 'red'},
            'critical': {'color': 'red', 'bold': True},
        }
        field_styles = {
            'asctime': {'color': 'green'},
            'levelname': {'bold': True},
            'message': {'color': 'green'}
        }
        log_format = "%(asctime)s %(levelname)s %(message)s"
        coloredlogs.install(
            level=level,
            logger=self.logger,
            fmt=log_format,
            level_styles=level_styles,
            field_styles=field_styles,
            isatty=True
        )

    def debug(self, message, show_log: bool = True):
        if show_log:
            self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


LOGGER = Logger.get_instance()
