import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Создаём папку logs, если её нет
os.makedirs("logs", exist_ok=True)

# Настройка форматирования
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

# Вывод в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Запись в файл с ротацией (ежедневно)
file_handler = TimedRotatingFileHandler(
    "logs/app.log", when="midnight", interval=1, backupCount=30, encoding="utf-8"
)
file_handler.setFormatter(formatter)

# Настройка логгера
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
