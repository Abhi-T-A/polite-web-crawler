import logging
from pathlib import Path

# Create logs directory
Path("logs").mkdir(exist_ok=True)

logger = logging.getLogger("PoliteScraper")
logger.setLevel(logging.INFO)

# Remove existing handlers (helps during reruns)
logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File
file_handler = logging.FileHandler("logs/scraper.log", encoding="utf-8")
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)