"""Logging"""

# stdlib
from logging import getLogger, StreamHandler
from os import environ


logger = getLogger()
"""Root logger"""

logger.addHandler(StreamHandler())
logger.setLevel(environ.get("LOG_LEVEL", "INFO"))
