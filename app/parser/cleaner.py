from urllib.parse import urljoin

from app.config import settings


class Cleaner:
    """
    Responsible for cleaning and transforming extracted data.
    """

    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    @staticmethod
    def clean_title(title: str) -> str:
        return title.strip()

    @staticmethod
    def clean_price(price: str) -> float:
        """
        Convert:
        £51.77
        ↓
        51.77
        """
        return float(price.replace("£", "").strip())

    @staticmethod
    def clean_rating(rating: str) -> int:
        """
        Convert:
        Three
        ↓
        3
        """
        return Cleaner.RATING_MAP.get(rating, 0)

    @staticmethod
    def absolute_url(relative_url: str) -> str:
        """
        Convert relative URL to absolute URL.
        """
        return urljoin(settings.BASE_URL, relative_url)