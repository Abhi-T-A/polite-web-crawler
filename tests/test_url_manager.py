from app.crawler.url_manager import URLManager


def test_normalize_url():
    mgr = URLManager()
    
    # Casing, fragments, parameters, trailing slash
    raw = "HTTP://Books.ToScrape.com/catalogue/page-1.html/?b=2&a=1#section"
    normalized = mgr.normalize_url(raw)
    
    assert normalized == "http://books.toscrape.com/catalogue/page-1.html?a=1&b=2"


def test_visited_tracking():
    mgr = URLManager()
    url = "https://books.toscrape.com/index.html"

    assert not mgr.is_visited(url)
    assert mgr.add_visited(url) is True
    assert mgr.is_visited(url) is True
    assert mgr.add_visited(url) is False
    assert mgr.visited_count == 1

    mgr.reset()
    assert mgr.visited_count == 0
    assert not mgr.is_visited(url)
