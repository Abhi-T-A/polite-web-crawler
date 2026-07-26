from typing import List
from pydantic import BaseModel, ConfigDict, HttpUrl


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    price: float
    rating: int
    image_url: HttpUrl
    product_url: HttpUrl


class BookListResponse(BaseModel):
    total: int
    page: int
    limit: int
    books: List[BookResponse]


class StatsResponse(BaseModel):
    total_books: int
    average_price: float
    rating_distribution: dict[int, int]
