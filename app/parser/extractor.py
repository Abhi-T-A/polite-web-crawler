from bs4 import BeautifulSoup

from app.models.record import BookRecord

from app.parser.cleaner import Cleaner

from app.parser.cleaner import Cleaner

class Extractor:

    @staticmethod
    def extract_books(soup: BeautifulSoup):

        books = []

        articles = soup.select("article.product_pod")

        for article in articles:

            title = article.h3.a["title"]

            price = article.select_one(".price_color").text.strip()

            rating = article.select_one(".star-rating")["class"][1]

            image_url = article.img["src"]

            product_url = article.h3.a["href"]

            books.append(
    BookRecord(
        title=Cleaner.clean_title(title),
        price=Cleaner.clean_price(price),
        rating=Cleaner.clean_rating(rating),
        image_url=Cleaner.absolute_url(image_url),
        product_url=Cleaner.absolute_url(product_url),
    )
)

        return books