from loguru import logger
import sys
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logger.remove()
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan}:{function}:{line} - <level>{message}</level>")
logger.add("logs/app.log", rotation="10 MB", retention="10 days", level="DEBUG", encoding="utf-8")
