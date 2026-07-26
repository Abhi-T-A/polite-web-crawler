from app.crawler.scheduler import Scheduler
from bs4 import BeautifulSoup


def test_scheduler_next_page():
    html_with_next = """
    <ul class="pager">
        <li class="next"><a href="page-2.html">next</a></li>
    </ul>
    """
    soup = BeautifulSoup(html_with_next, "lxml")
    next_url = Scheduler.get_next_page(soup, "https://books.toscrape.com/catalogue/page-1.html")
    assert next_url == "https://books.toscrape.com/catalogue/page-2.html"


def test_scheduler_no_next_page():
    html_without_next = "<ul class='pager'></ul>"
    soup = BeautifulSoup(html_without_next, "lxml")
    next_url = Scheduler.get_next_page(soup, "https://books.toscrape.com/catalogue/page-50.html")
    assert next_url is None
