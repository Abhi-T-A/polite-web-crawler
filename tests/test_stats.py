import time
from app.utils.stats import CrawlStats


def test_crawl_stats_metrics():
    stats = CrawlStats()
    stats.start()
    time.sleep(0.05)
    
    stats.record_page(books_count=20, response_time=0.5)
    stats.record_page(books_count=20, response_time=0.3)
    stats.record_failure()
    stats.stop()

    assert stats.pages_crawled == 2
    assert stats.books_extracted == 40
    assert stats.failed_requests == 1
    assert stats.duration > 0
    assert stats.avg_response_time == 0.4
    assert stats.success_rate == 66.67
    
    report = stats.generate_report()
    assert "Crawl Report" in report
    assert "Books Extracted    : 40" in report
