from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from app.api.schemas.book import BookListResponse, BookResponse, StatsResponse
from app.api.services.book_service import BookService

router = APIRouter()
book_service = BookService()


@router.get("/books", response_model=BookListResponse)
def get_books(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    min_rating: Optional[int] = Query(None, ge=1, le=5, description="Minimum rating (1-5)"),
    sort_by: Optional[str] = Query(
        None, description="Sort order: 'price_asc', 'price_desc', 'rating_desc'"
    ),
):
    """
    Retrieve paginated list of scraped books with optional price/rating filtering and sorting.
    """
    total, books = book_service.get_books(
        page=page,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        sort_by=sort_by,
    )
    return BookListResponse(total=total, page=page, limit=limit, books=books)


@router.get("/books/search", response_model=BookListResponse)
def search_books(
    q: str = Query(..., min_length=1, description="Search title query keyword"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """
    Search books by title keyword.
    """
    total, books = book_service.search_books(query_str=q, page=page, limit=limit)
    return BookListResponse(total=total, page=page, limit=limit, books=books)


@router.get("/books/{book_id}", response_model=BookResponse)
def get_book_by_id(book_id: int):
    """
    Retrieve single book details by ID.
    """
    book = book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/stats", response_model=StatsResponse)
def get_stats():
    """
    Retrieve dataset summary statistics (total books, average price, rating breakdown).
    """
    stats = book_service.get_stats()
    return StatsResponse(**stats)
