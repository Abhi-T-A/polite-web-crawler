from pydantic import BaseModel, HttpUrl


class BookRecord(BaseModel):
    title: str
    price: float
    rating: int
    image_url: HttpUrl
    product_url: HttpUrl