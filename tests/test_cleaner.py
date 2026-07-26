import pytest
from app.parser.cleaner import Cleaner


def test_clean_title():
    assert Cleaner.clean_title("  A Light in the Attic  ") == "A Light in the Attic"


def test_clean_price():
    assert Cleaner.clean_price("£51.77") == 51.77
    assert Cleaner.clean_price("£0.99 ") == 0.99


def test_clean_rating():
    assert Cleaner.clean_rating("One") == 1
    assert Cleaner.clean_rating("Two") == 2
    assert Cleaner.clean_rating("Three") == 3
    assert Cleaner.clean_rating("Four") == 4
    assert Cleaner.clean_rating("Five") == 5
    assert Cleaner.clean_rating("Unknown") == 0


def test_absolute_url():
    url = Cleaner.absolute_url("catalogue/a-light-in-the-attic_1000/index.html")
    assert url.startswith("https://books.toscrape.com/")
    assert "a-light-in-the-attic_1000/index.html" in url
