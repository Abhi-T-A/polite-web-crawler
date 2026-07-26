import csv
from pathlib import Path
from typing import List

from app.config import settings
from app.models.record import BookRecord
from app.storage.base import Storage
from app.utils.logger import logger


class CSVStorage(Storage):
    """
    Saves scraped records to a CSV file.
    """

    def __init__(self, output_file: str | None = None):
        self.output_file = output_file or settings.OUTPUT_CSV

    def save(self, records: List[BookRecord]) -> None:
        """Export records to CSV format with headers."""
        if not records:
            return

        target_path = Path(self.output_file)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = ["title", "price", "rating", "image_url", "product_url"]

        with open(target_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                row = record.model_dump(mode="json")
                writer.writerow(row)

        logger.info(f"Saved {len(records)} records to CSV ({self.output_file})")

    def close(self) -> None:
        """CSV storage cleanup (no-op)."""
        pass
