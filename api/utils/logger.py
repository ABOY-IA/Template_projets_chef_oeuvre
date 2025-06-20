import os
import sys
from loguru import logger

LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "logs", "api.log")
)

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

logger.add(
    LOG_PATH,
    rotation="10 MB",
    retention="10 days",
    level="DEBUG",
    enqueue=True,
    backtrace=True,
    diagnose=True,
)
