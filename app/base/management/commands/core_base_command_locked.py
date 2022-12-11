__all__ = ['CoreBaseCommandLocked']

import os
import sys

import fcntl
from django.conf import settings

from .core_base_command import CoreBaseCommand


class CoreBaseCommandLocked(CoreBaseCommand):

    def get_lock_name(self, **options):
        return sys.argv[1]

    def execute(self, *args, **options):

        lock_name = self.get_lock_name(**options)
        try:
            lock_file_path = os.path.join(settings.LOCKS_DIR, "{0}.lock".format(lock_name))
            f = open(lock_file_path, 'w')
            fcntl.lockf(f, fcntl.LOCK_EX + fcntl.LOCK_NB)
        except IOError:
            self.logger.warning(f"Previous {self.name} command process has not finished yet. Abort starting...")
            exit(1)

        return super().execute(*args, **options)
