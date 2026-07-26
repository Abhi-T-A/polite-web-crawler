from bs4 import BeautifulSoup


class HTMLParser:
    """
    Converts raw HTML into a BeautifulSoup object.
    """

    @staticmethod
    def parse(html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")