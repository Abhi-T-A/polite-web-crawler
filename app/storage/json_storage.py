import json
from pathlib import Path
from typing import List

from app.config import settings
from app.models.record import BookRecord
from app.storage.base import Storage
from app.utils.logger import logger


class JSONStorage(Storage):
    """
    Saves scraped records to a JSON file.
    """

    def __init__(self, output_file: str | None = None):
        self.output_file = output_file or settings.OUTPUT_JSON

    def save(self, records: List[BookRecord]) -> None:
        """Persist records to the specified JSON file."""
        if not records:
            return

        target_path = Path(self.output_file)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        data = [record.model_dump(mode="json") for record in records]

        with open(target_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        logger.info(f"Saved {len(records)} records to JSON ({self.output_file})")

    def close(self) -> None:
        """JSON storage cleanup (no-op)."""
        pass