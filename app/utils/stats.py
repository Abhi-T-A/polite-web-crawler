import time
from app.utils.logger import logger


class CrawlStats:
    """
    Collects metrics during the crawl and formats a summary report.
    """

    def __init__(self):
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.pages_crawled: int = 0
        self.books_extracted: int = 0
        self.failed_requests: int = 0
        self.response_times: list[float] = []

    def start(self) -> None:
        """Mark the start of the crawl session."""
        self.start_time = time.time()
        self.end_time = None

    def stop(self) -> None:
        """Mark the end of the crawl session."""
        self.end_time = time.time()

    def record_page(self, books_count: int, response_time: float = 0.0) -> None:
        """Record statistics for a successfully fetched and parsed page."""
        self.pages_crawled += 1
        self.books_extracted += books_count
        if response_time > 0:
            self.response_times.append(response_time)

    def record_failure(self) -> None:
        """Record a failed page request."""
        self.failed_requests += 1

    @property
    def duration(self) -> float:
        """Calculates total duration in seconds."""
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time is not None else time.time()
        return round(end - self.start_time, 2)

    @property
    def avg_response_time(self) -> float:
        """Calculates average response time in seconds."""
        if not self.response_times:
            return 0.0
        return round(sum(self.response_times) / len(self.response_times), 3)

    @property
    def success_rate(self) -> float:
        """Calculates percentage of successful requests."""
        total = self.pages_crawled + self.failed_requests
        if total == 0:
            return 0.0
        return round((self.pages_crawled / total) * 100, 2)

    def generate_report(self) -> str:
        """Generates a human-readable text report summarizing the crawl."""
        report = (
            "\n"
            + "=" * 42 + "\n"
            + "           Crawl Report\n"
            + "=" * 42 + "\n"
            + f"Pages Crawled      : {self.pages_crawled}\n"
            + f"Books Extracted    : {self.books_extracted}\n"
            + f"Failed Requests    : {self.failed_requests}\n"
            + f"Success Rate       : {self.success_rate}%\n"
            + f"Avg Response Time  : {self.avg_response_time} sec\n"
            + f"Total Duration     : {self.duration} sec\n"
            + "=" * 42
        )
        return report

    def print_report(self) -> None:
        """Logs the summary report."""
        logger.info(self.generate_report())
