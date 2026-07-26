import time
import logging
from typing import List, Optional

from app.config import settings
from app.crawler.fetcher import Fetcher
from app.crawler.scheduler import Scheduler
from app.crawler.robots import RobotsChecker
from app.crawler.limiter import RateLimiter
from app.crawler.url_manager import URLManager

from app.parser.html_parser import HTMLParser
from app.parser.extractor import Extractor

from app.storage.base import Storage
from app.storage.json_storage import JSONStorage
from app.storage.sqlite_storage import SQLiteStorage
from app.storage.csv_storage import CSVStorage

from app.utils.logger import logger
from app.utils.stats import CrawlStats


def run_crawler(
    limit: Optional[int] = None,
    delay: Optional[float] = None,
    use_sqlite: bool = True,
    use_json: bool = True,
    use_csv: bool = False,
    verbose: bool = False,
) -> CrawlStats:
    """
    Main execution entry point for the Polite Web Crawler.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    request_delay = delay if delay is not None else settings.REQUEST_DELAY

    # Initialize Crawler Components
    fetcher = Fetcher()
    url_manager = URLManager()
    stats = CrawlStats()
    robots = RobotsChecker(settings.USER_AGENT)
    robots.load(settings.BASE_URL)

    # Configure Active Storage Backends
    storage_backends: List[Storage] = []
    if use_sqlite:
        storage_backends.append(SQLiteStorage())
    if use_json:
        storage_backends.append(JSONStorage())
    if use_csv:
        storage_backends.append(CSVStorage())

    all_books = []
    current_url = settings.BASE_URL
    page_number = 1

    stats.start()
    logger.info("Starting Polite Web Crawler session...")

    try:
        while current_url:
            if limit and page_number > limit:
                logger.info(f"Reached page limit limit={limit}. Stopping crawler.")
                break

            canonical_url = url_manager.normalize_url(current_url)
            if url_manager.is_visited(canonical_url):
                logger.warning(f"URL already visited: {canonical_url}. Skipping.")
                break

            if not robots.can_fetch(current_url):
                logger.warning(f"Blocked by robots.txt: {current_url}. Stopping crawler.")
                stats.record_failure()
                break

            logger.info("=" * 60)
            logger.info(f"Crawling Page {page_number}: {current_url}")

            url_manager.add_visited(current_url)

            # Fetch page and measure duration
            t0 = time.time()
            html = fetcher.fetch(current_url)
            fetch_duration = time.time() - t0

            if not html:
                logger.error(f"Failed to fetch page: {current_url}")
                stats.record_failure()
                break

            # Rate Limiter
            logger.info(f"Sleeping for {request_delay} seconds...")
            time.sleep(request_delay)

            # Parse HTML
            soup = HTMLParser.parse(html)
            books = Extractor.extract_books(soup)

            stats.record_page(len(books), response_time=fetch_duration)
            logger.info(f"Extracted {len(books)} books on page {page_number}")

            all_books.extend(books)

            # Save page results to active storage backends
            for backend in storage_backends:
                backend.save(books)

            # Discover next page link
            current_url = Scheduler.get_next_page(soup, current_url)
            page_number += 1

    finally:
        stats.stop()
        
        # Save complete dataset to file-based exporters if active
        for backend in storage_backends:
            if isinstance(backend, (JSONStorage, CSVStorage)):
                backend.save(all_books)
            backend.close()

        fetcher.close()
        stats.print_report()

    return stats


def main():
    """Fallback entry point calling run_crawler with default parameters."""
    run_crawler()


if __name__ == "__main__":
    main()