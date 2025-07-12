# src/utils/logging.py

import sys

import picologging
import structlog

# structlog konfiguratsiyasi
structlog.configure(
    cache_logger_on_first_use=True,
    wrapper_class=structlog.make_filtering_bound_logger(picologging.INFO),
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
        structlog.dev.ConsoleRenderer(exception_formatter=structlog.dev.better_traceback),
    ],
)

log = structlog.wrap_logger(logger=picologging.getLogger())
# picologging konfiguratsiyasi
picologging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=picologging.INFO,
)

# structlog logger obyekti

