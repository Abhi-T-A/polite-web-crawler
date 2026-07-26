from bs4 import BeautifulSoup
from app.parser.extractor import Extractor


SAMPLE_HTML = """
<ol class="row">
    <li class="col-xs-6 col-sm-4 col-md-3 col-lg-3">
        <article class="product_pod">
            <div class="image_container">
                <a href="catalogue/a-light-in-the-attic_1000/index.html">
                    <img src="media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg" alt="A Light in the Attic">
                </a>
            </div>
            <p class="star-rating Three"></p>
            <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the Attic</a></h3>
            <div class="product_price">
                <p class="price_color">£51.77</p>
            </div>
        </article>
    </li>
</ol>
"""


def test_extract_books():
    soup = BeautifulSoup(SAMPLE_HTML, "lxml")
    books = Extractor.extract_books(soup)

    assert len(books) == 1
    book = books[0]
    assert book.title == "A Light in the Attic"
    assert book.price == 51.77
    assert book.rating == 3
    assert "books.toscrape.com" in str(book.image_url)
    assert "a-light-in-the-attic_1000" in str(book.product_url)
