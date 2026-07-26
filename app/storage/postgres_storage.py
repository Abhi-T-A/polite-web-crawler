import os
from typing import List
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings
from app.models.record import BookRecord
from app.storage.base import Storage
from app.utils.logger import logger

Base = declarative_base()


class BookModel(Base):
    """
    SQLAlchemy ORM Model representing the books database table.
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(512), nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Integer, nullable=False)
    image_url = Column(String(1024), nullable=False)
    product_url = Column(String(1024), nullable=False, unique=True, index=True)


class PostgresStorage(Storage):
    """
    PostgreSQL persistence backend implementing SQLAlchemy ORM with deduplication.
    """

    def __init__(self, connection_url: str | None = None):
        url = connection_url or os.getenv(
            "POSTGRES_URL",
            "postgresql://postgres:postgres@localhost:5432/polite_scraper",
        )

        # Fallback to SQLite in-memory if testing without PostgreSQL driver
        if url.startswith("sqlite"):
            self.engine = create_engine(url)
        else:
            try:
                self.engine = create_engine(url, pool_size=10, max_overflow=20)
            except Exception as e:
                logger.warning(f"PostgreSQL connection failed ({e}). Falling back to SQLite memory.")
                self.engine = create_engine("sqlite:///:memory:")

        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def save(self, records: List[BookRecord]) -> None:
        """
        Persist a list of BookRecord objects into the database with duplicate handling.
        """
        if not records:
            return

        session = self.SessionLocal()
        inserted_count = 0
        skipped_count = 0

        try:
            for record in records:
                prod_url = str(record.product_url)
                # Check for existing record by unique product_url
                existing = (
                    session.query(BookModel)
                    .filter(BookModel.product_url == prod_url)
                    .first()
                )

                if existing:
                    skipped_count += 1
                    continue

                book_obj = BookModel(
                    title=record.title,
                    price=record.price,
                    rating=record.rating,
                    image_url=str(record.image_url),
                    product_url=prod_url,
                )
                session.add(book_obj)
                inserted_count += 1

            session.commit()
            logger.info(
                f"SQLAlchemy Storage: Inserted {inserted_count} records"
                + (f" ({skipped_count} duplicates skipped)" if skipped_count > 0 else "")
            )
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save records in SQLAlchemy Storage: {e}")
            raise
        finally:
            session.close()

    def close(self) -> None:
        """Dispose of the SQLAlchemy connection engine pool."""
        if hasattr(self, "engine"):
            self.engine.dispose()
