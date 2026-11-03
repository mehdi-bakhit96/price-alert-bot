import sys
from loguru import logger

# تنظیم لاگر استاندارد
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/tracker.log",
    rotation="5 MB",
    retention="10 days",
    level="DEBUG",
    encoding="utf-8"
)
