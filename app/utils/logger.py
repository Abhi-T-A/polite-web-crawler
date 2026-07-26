import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

logger = logging.getLogger("PoliteScraper")
logger.setLevel(logging.INFO)

# Clear existing handlers during re-initialization
logger.handlers.clear()

formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

# 1. Console Stream Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

# 2. Rotating Main Log File (Info + Debug + Warning + Error)
main_file_handler = RotatingFileHandler(
    "logs/scraper.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3,
    encoding="utf-8",
)
main_file_handler.setFormatter(formatter)
main_file_handler.setLevel(logging.DEBUG)

# 3. Rotating Dedicated Error Log File (Warning + Error Only)
error_file_handler = RotatingFileHandler(
    "logs/error.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3,
    encoding="utf-8",
)
error_file_handler.setFormatter(formatter)
error_file_handler.setLevel(logging.WARNING)

# Attach Handlers
logger.addHandler(console_handler)
logger.addHandler(main_file_handler)
logger.addHandler(error_file_handler)