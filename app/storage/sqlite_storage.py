import sqlite3
from pathlib import Path

from app.config import settings
from app.utils.logger import logger


class SQLiteStorage:

    def __init__(self):
        Path(settings.DATABASE_PATH).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            settings.DATABASE_PATH
        )

        self.cursor = self.connection.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            price REAL NOT NULL,

            rating INTEGER NOT NULL,

            image_url TEXT NOT NULL,

            product_url TEXT NOT NULL
        );
        """)

        self.connection.commit()

    def save(self, books):

        self.cursor.executemany("""

        INSERT INTO books
        (
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

            for book in books

        ])

        self.connection.commit()

        logger.info(f"Inserted {len(books)} books into SQLite.")

    def close(self):
        self.connection.close()