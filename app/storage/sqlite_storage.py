import sqlite3
from pathlib import Path
from typing import List

from app.config import settings
from app.models.record import BookRecord
from app.storage.base import Storage
from app.utils.logger import logger


class SQLiteStorage(Storage):
    """
    SQLite persistence backend implementing unique constraint deduplication.
    """

    def __init__(self, db_path: str | None = None):
        target_path = db_path or settings.DATABASE_PATH
        Path(target_path).parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(target_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self) -> None:
        """Create table if not exists with product_url UNIQUE constraint."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            rating INTEGER NOT NULL,
            image_url TEXT NOT NULL,
            product_url TEXT NOT NULL UNIQUE
        );
        """)
        self.connection.commit()

    def save(self, records: List[BookRecord]) -> None:
        """Save records into SQLite using INSERT OR IGNORE for duplicate prevention."""
        if not records:
            return

        initial_changes = self.connection.total_changes

        self.cursor.executemany("""
        INSERT OR IGNORE INTO books (
            title,
            price,
            rating,
            image_url,
            product_url
        )
        VALUES (?, ?, ?, ?, ?)
        """, [
            (
                book.title,
                book.price,
                book.rating,
                str(book.image_url),
                str(book.product_url)
            )
            for book in records
        ])

        self.connection.commit()
        inserted_count = self.connection.total_changes - initial_changes
        skipped_count = len(records) - inserted_count

        logger.info(
            f"SQLite Storage: Inserted {inserted_count} new books"
            + (f" ({skipped_count} duplicates skipped)" if skipped_count > 0 else "")
        )

    def close(self) -> None:
        """Close SQLite database connection."""
        if self.connection:
            self.connection.close()