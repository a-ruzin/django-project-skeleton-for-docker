import logging.config
import sys
import time
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class CoreBaseCommandError(CommandError):
    pass


class CoreBaseCommand(BaseCommand):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.name = sys.argv[1]
        self.logger = self._get_logger()
        self.__rewrite_root_logger()

        self.options = None
        super(CoreBaseCommand, self).__init__(*args, **kwargs)

    def _get_logger(self) -> logging.Logger:
        logger_name = f"app.command.{self.name}"

        if logger_name in settings.LOGGING["loggers"]:
            return logging.getLogger(logger_name)

        return logging.getLogger("app.command")

    def __rewrite_root_logger(self) -> None:
        root_logger = logging.getLogger()
        root_logger.handlers = self.logger.handlers
        root_logger.setLevel(self.logger.level)

    def execute(self, *args: Any, **options: Any) -> Any:
        started = time.perf_counter()
        try:
            self.logger.info(f"New {self.name} command started at {timezone.now()} >>>>>>")
            result = super(CoreBaseCommand, self).execute(*args, **options)
            duration = time.perf_counter() - started
            self.logger.info(f"The {self.name} command finished at {timezone.now()} <<<<<< in {duration} seconds")
            return result
        except Exception as e:
            self.logger.exception(e)
            duration = time.perf_counter() - started
            self.logger.info(f"The {self.name} command crashed at {timezone.now()} <<<<<< in {duration} seconds")
            raise
