import sys
import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    """Создаёт и настраивает логгер для API."""

    # Создаём логгер
    logger = logging.getLogger("api_logger")
    logger.setLevel(logging.INFO)

    # Формат логов
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Лог в файл с ротацией (макс. 5MB, хранится 3 файла)
    file_handler = RotatingFileHandler("logs/api.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Лог в консоль (stdout)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Добавляем обработчики в логгер
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
