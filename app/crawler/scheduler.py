from urllib.parse import urljoin

from bs4 import BeautifulSoup


class Scheduler:
    """
    Finds the next page URL.
    """

    @staticmethod
    def get_next_page(soup: BeautifulSoup, current_url: str):

        next_button = soup.select_one("li.next a")

        if next_button is None:
            return None

        href = next_button.get("href")

        return urljoin(current_url, href)