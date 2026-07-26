import asyncio
import time
from typing import Dict

from app.config import settings
from app.crawler.fetcher import Fetcher
from app.crawler.async_fetcher import AsyncFetcher
from app.utils.logger import logger


def benchmark_sequential(num_pages: int = 5) -> Dict[str, float]:
    """
    Run sequential crawl benchmark across N pages.
    """
    urls = [
        f"https://books.toscrape.com/catalogue/page-{i}.html"
        for i in range(1, num_pages + 1)
    ]

    fetcher = Fetcher()
    start_time = time.time()
    success = 0
    failed = 0
    response_times = []

    try:
        for url in urls:
            t0 = time.time()
            res = fetcher.fetch(url)
            duration = time.time() - t0
            if res:
                success += 1
                response_times.append(duration)
            else:
                failed += 1
    finally:
        fetcher.close()

    total_time = round(time.time() - start_time, 2)
    avg_resp = round(sum(response_times) / len(response_times), 3) if response_times else 0.0

    return {
        "total_time": total_time,
        "req_per_sec": round(num_pages / total_time, 2) if total_time > 0 else 0.0,
        "pages_per_sec": round(success / total_time, 2) if total_time > 0 else 0.0,
        "avg_resp_time": avg_resp,
        "success_rate": round((success / num_pages) * 100, 2),
        "failed_requests": failed,
    }


async def benchmark_async(num_pages: int = 5, concurrency: int = 5) -> Dict[str, float]:
    """
    Run asynchronous concurrent crawl benchmark across N pages.
    """
    urls = [
        f"https://books.toscrape.com/catalogue/page-{i}.html"
        for i in range(1, num_pages + 1)
    ]

    start_time = time.time()
    success = 0
    failed = 0

    async with AsyncFetcher(concurrency_limit=concurrency) as fetcher:
        tasks = [fetcher.fetch(url) for url in urls]
        results = await asyncio.gather(*tasks)

    for res in results:
        if res:
            success += 1
        else:
            failed += 1

    total_time = round(time.time() - start_time, 2)
    avg_resp = round(total_time / num_pages, 3) if num_pages > 0 else 0.0

    return {
        "total_time": total_time,
        "req_per_sec": round(num_pages / total_time, 2) if total_time > 0 else 0.0,
        "pages_per_sec": round(success / total_time, 2) if total_time > 0 else 0.0,
        "avg_resp_time": avg_resp,
        "success_rate": round((success / num_pages) * 100, 2),
        "failed_requests": failed,
    }


def print_benchmark_table(seq: Dict[str, float], async_res: Dict[str, float]) -> None:
    """
    Formats and prints a side-by-side performance benchmarking report.
    """
    report = (
        "\n"
        + "=" * 55 + "\n"
        + "       Performance Benchmark Comparison Report\n"
        + "=" * 55 + "\n"
        + f"{'Metric':<25} | {'Sequential':<12} | {'Async':<12}\n"
        + "-" * 55 + "\n"
        + f"{'Total Duration (sec)':<25} | {seq['total_time']:<12} | {async_res['total_time']:<12}\n"
        + f"{'Requests / Sec':<25} | {seq['req_per_sec']:<12} | {async_res['req_per_sec']:<12}\n"
        + f"{'Pages / Sec':<25} | {seq['pages_per_sec']:<12} | {async_res['pages_per_sec']:<12}\n"
        + f"{'Avg Response Time (s)':<25} | {seq['avg_resp_time']:<12} | {async_res['avg_resp_time']:<12}\n"
        + f"{'Success Rate (%)':<25} | {seq['success_rate']:<12} | {async_res['success_rate']:<12}\n"
        + f"{'Failed Requests':<25} | {seq['failed_requests']:<12} | {async_res['failed_requests']:<12}\n"
        + "=" * 55
    )
    print(report)
    logger.info(report)


def run_benchmark(num_pages: int = 5):
    """
    Run side-by-side benchmark comparing Sequential vs Async crawler engines.
    """
    logger.info(f"Running Sequential Benchmark across {num_pages} pages...")
    seq_metrics = benchmark_sequential(num_pages=num_pages)

    logger.info(f"Running Async Benchmark across {num_pages} pages...")
    async_metrics = asyncio.run(benchmark_async(num_pages=num_pages))

    print_benchmark_table(seq_metrics, async_metrics)


if __name__ == "__main__":
    run_benchmark()
