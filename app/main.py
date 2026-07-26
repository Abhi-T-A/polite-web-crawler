from app.config import settings

from app.crawler.fetcher import Fetcher
from app.crawler.scheduler import Scheduler
from app.crawler.robots import RobotsChecker
from app.crawler.limiter import RateLimiter

from app.parser.html_parser import HTMLParser
from app.parser.extractor import Extractor

from app.storage.json_storage import JSONStorage
from app.storage.sqlite_storage import SQLiteStorage

from app.utils.logger import logger


def main():

    fetcher = Fetcher()
    sqlite = SQLiteStorage()

    robots = RobotsChecker(settings.USER_AGENT)
    robots.load(settings.BASE_URL)

    current_url = settings.BASE_URL

    all_books = []

    page_number = 1

    try:

        while current_url:

            # Check robots.txt
            if not robots.can_fetch(current_url):
                logger.warning("Blocked by robots.txt. Stopping crawler.")
                break

            logger.info("=" * 60)
            logger.info(f"Crawling Page {page_number}")
            logger.info(current_url)

            # Fetch page
            html = fetcher.fetch(current_url)

            if not html:
                logger.error("Failed to fetch page.")
                break

            # Respect crawl delay
            RateLimiter.wait()

            # Parse HTML
            soup = HTMLParser.parse(html)

            # Extract books
            books = Extractor.extract_books(soup)

            logger.info(f"Books on page: {len(books)}")

            # Store in memory
            all_books.extend(books)

            # Save to SQLite
            sqlite.save(books)

            # Get next page
            current_url = Scheduler.get_next_page(
                soup,
                current_url
            )

            page_number += 1

        # Save all books to JSON
        JSONStorage.save(
            all_books,
            settings.OUTPUT_JSON
        )

        logger.info("=" * 60)
        logger.info(f"Total Books Crawled : {len(all_books)}")

    finally:

        sqlite.close()
        fetcher.close()

        logger.info("Crawler Finished Successfully.")


if __name__ == "__main__":
    main()