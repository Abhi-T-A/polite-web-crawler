import json
import csv
import pytest
from app.models.record import BookRecord
from app.storage.sqlite_storage import SQLiteStorage
from app.storage.json_storage import JSONStorage
from app.storage.csv_storage import CSVStorage


@pytest.fixture
def sample_books():
    return [
        BookRecord(
            title="Book One",
            price=19.99,
            rating=5,
            image_url="https://example.com/img1.jpg",
            product_url="https://example.com/book1.html",
        ),
        BookRecord(
            title="Book Two",
            price=29.99,
            rating=4,
            image_url="https://example.com/img2.jpg",
            product_url="https://example.com/book2.html",
        ),
    ]


def test_sqlite_storage_deduplication(tmp_path, sample_books):
    db_file = str(tmp_path / "test.db")
    storage = SQLiteStorage(db_path=db_file)

    # First insert
    storage.save(sample_books)
    
    storage.cursor.execute("SELECT COUNT(*) FROM books")
    assert storage.cursor.fetchone()[0] == 2

    # Second insert with duplicate product_url
    storage.save(sample_books)
    storage.cursor.execute("SELECT COUNT(*) FROM books")
    assert storage.cursor.fetchone()[0] == 2  # Deduplicated

    storage.close()


def test_json_storage(tmp_path, sample_books):
    json_file = str(tmp_path / "output.json")
    storage = JSONStorage(output_file=json_file)
    storage.save(sample_books)

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["title"] == "Book One"
    assert data[0]["price"] == 19.99


def test_csv_storage(tmp_path, sample_books):
    csv_file = str(tmp_path / "output.csv")
    storage = CSVStorage(output_file=csv_file)
    storage.save(sample_books)

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 2
    assert reader[0]["title"] == "Book One"
    assert float(reader[0]["price"]) == 19.99
