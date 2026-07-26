import time

from app.config import settings
from app.crawler.fetcher import Fetcher
from app.crawler.scheduler import Scheduler
from app.crawler.robots import RobotsChecker
from app.crawler.limiter import RateLimiter
from app.crawler.url_manager import URLManager

from app.parser.html_parser import HTMLParser
from app.parser.extractor import Extractor

from app.storage.sqlite_storage import SQLiteStorage
from app.storage.json_storage import JSONStorage

from app.utils.logger import logger
from app.utils.stats import CrawlStats


def main():
    """
    Workshop Scraping Pipeline:
    Fetch -> Parse -> Extract -> Clean -> Structure -> Save
    """
    fetcher = Fetcher()
    url_manager = URLManager()
    stats = CrawlStats()
    sqlite_storage = SQLiteStorage()
    json_storage = JSONStorage()

    robots = RobotsChecker(settings.USER_AGENT)
    robots.load(settings.BASE_URL)

    current_url = settings.BASE_URL
    all_books = []
    page_number = 1

    stats.start()
    logger.info("Starting Polite Web Crawler...")

    try:
        while current_url:
            canonical_url = url_manager.normalize_url(current_url)

            # Check if URL was already visited
            if url_manager.is_visited(canonical_url):
                logger.warning(f"URL already visited: {canonical_url}. Skipping.")
                break

            # Verify robots.txt compliance
            if not robots.can_fetch(current_url):
                logger.warning(f"Blocked by robots.txt: {current_url}. Stopping crawler.")
                stats.record_failure()
                break

            logger.info("=" * 60)
            logger.info(f"Crawling Page {page_number}: {current_url}")

            url_manager.add_visited(current_url)

            # 1. FETCH
            t0 = time.time()
            html = fetcher.fetch(current_url)
            fetch_duration = time.time() - t0

            if not html:
                logger.error(f"Failed to fetch page: {current_url}")
                stats.record_failure()
                break

            # Polite Rate Limiting Delay
            RateLimiter.wait()

            # 2. PARSE HTML
            soup = HTMLParser.parse(html)

            # 3. EXTRACT & CLEAN DATA into Pydantic BookRecord models
            books = Extractor.extract_books(soup)

            stats.record_page(len(books), response_time=fetch_duration)
            logger.info(f"Extracted {len(books)} structured records on Page {page_number}")

            all_books.extend(books)

            # 4. SAVE TO SQLITE (Database Storage)
            sqlite_storage.save(books)

            # Discover next page link
            current_url = Scheduler.get_next_page(soup, current_url)
            page_number += 1

        # 5. SAVE TO JSON (File Export)
        json_storage.save(all_books)

    finally:
        stats.stop()
        sqlite_storage.close()
        json_storage.close()
        fetcher.close()

        stats.print_report()
        logger.info("Crawler finished successfully.")


if __name__ == "__main__":
    main()