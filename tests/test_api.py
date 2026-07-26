from fastapi.testclient import TestClient
from app.api.main import app
from app.storage.sqlite_storage import SQLiteStorage
from app.models.record import BookRecord

client = TestClient(app)


def setup_module(module):
    # Ensure test SQLite DB exists with sample data
    storage = SQLiteStorage()
    sample_books = [
        BookRecord(
            title="Python Testing Cookbook",
            price=35.00,
            rating=5,
            image_url="https://example.com/p1.jpg",
            product_url="https://example.com/p1.html",
        ),
        BookRecord(
            title="Advanced Async Architecture",
            price=55.00,
            rating=4,
            image_url="https://example.com/p2.jpg",
            product_url="https://example.com/p2.html",
        ),
    ]
    storage.save(sample_books)
    storage.close()


def test_api_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_api_get_books():
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    data = response.json()
    assert "books" in data
    assert data["total"] >= 2


def test_api_search_books():
    response = client.get("/api/v1/books/search?q=Python")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert "Python" in data["books"][0]["title"]


def test_api_stats():
    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_books" in data
    assert "average_price" in data
