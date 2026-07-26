import pytest
from app.models.record import BookRecord
from app.storage.postgres_storage import PostgresStorage, BookModel


def test_postgres_storage_sqlite_fallback(tmp_path):
    db_url = f"sqlite:///{tmp_path}/test_orm.db"
    storage = PostgresStorage(connection_url=db_url)

    sample_records = [
        BookRecord(
            title="Postgres Book 1",
            price=49.99,
            rating=5,
            image_url="https://example.com/pg1.jpg",
            product_url="https://example.com/pg1.html",
        ),
        BookRecord(
            title="Postgres Book 2",
            price=29.99,
            rating=4,
            image_url="https://example.com/pg2.jpg",
            product_url="https://example.com/pg2.html",
        ),
    ]

    # First save
    storage.save(sample_records)

    session = storage.SessionLocal()
    count = session.query(BookModel).count()
    assert count == 2
    session.close()

    # Save again (test deduplication logic)
    storage.save(sample_records)

    session = storage.SessionLocal()
    count = session.query(BookModel).count()
    assert count == 2  # Deduplicated
    session.close()

    storage.close()
