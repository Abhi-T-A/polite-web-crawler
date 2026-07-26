import pytest
import httpx
from app.crawler.async_fetcher import AsyncFetcher


@pytest.mark.asyncio
async def test_async_fetcher_success():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="<html><body><h1>Async Test</h1></body></html>")

    fetcher = AsyncFetcher(concurrency_limit=2)
    fetcher.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    try:
        html = await fetcher.fetch("https://books.toscrape.com/test.html")
        assert html is not None
        assert "Async Test" in html
    finally:
        await fetcher.close()


@pytest.mark.asyncio
async def test_async_fetcher_failure_retry():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if len(calls) == 1:
            return httpx.Response(500)
        return httpx.Response(200, text="Recovered Content")

    fetcher = AsyncFetcher(concurrency_limit=2)
    fetcher.client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    try:
        html = await fetcher.fetch("https://books.toscrape.com/retry.html", retries=2)
        assert html == "Recovered Content"
        assert len(calls) == 2
    finally:
        await fetcher.close()
