"""Logging"""

# stdlib
from logging import getLogger, StreamHandler
from os import environ

# 3rd party
import colorlog


logger = getLogger()
"""Root logger"""

streamHandler = StreamHandler()
streamHandler.setFormatter(
    colorlog.ColoredFormatter(
        "{asctime} {log_color}{levelname:<7}{reset} "
        "{bold_white}{module}:{funcName}{reset} {cyan}\u00bb{reset} {message}",
        style="{",
    )
)
logger.addHandler(streamHandler)
logger.setLevel(environ.get("LOG_LEVEL", "INFO"))
