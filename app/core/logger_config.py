# app/logger_config.py
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logger():
    from loguru import logger

    logger.remove()

    # Логи в консоль
    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
    )

    # Основной лог-файл
    logger.add(
        LOG_DIR / "app.log",
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8",
        level="DEBUG",
        enqueue=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )

    return logger


logger = setup_logger()
