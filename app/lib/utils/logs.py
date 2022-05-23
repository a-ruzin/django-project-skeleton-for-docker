__all__ = ["get_command_folder_rotating_file_handler"]


def get_command_folder_rotating_file_handler(**kwargs):
    from django.conf import settings
    import sys
    import logging.handlers

    class LazyRotatingFileHandler(logging.handlers.RotatingFileHandler):
        def _open(self):
            (settings.LOGS_DIR / sys.argv[1]).mkdir(parents=True, exist_ok=True)
            return super()._open()

    if sys.argv[0].endswith('manage.py') and len(sys.argv) > 1:
        log_file_name = settings.LOGS_DIR / sys.argv[1] / f"{sys.argv[1]}.log"
        return LazyRotatingFileHandler(filename=log_file_name, **kwargs)
    else:
        return logging.NullHandler()
