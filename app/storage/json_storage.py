import json
from pathlib import Path

from app.utils.logger import logger


class JSONStorage:
    """
    Save scraped records to a JSON file.
    """

    @staticmethod
    def save(records, output_file: str):

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        data = [
            record.model_dump(mode="json")
            for record in records
        ]

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info(f"Saved {len(records)} records to {output_file}")