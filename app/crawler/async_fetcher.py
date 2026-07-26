import asyncio
import time
import httpx
from typing import Optional

from app.config import settings
from app.utils.logger import logger


class AsyncFetcher:
    """
    Asynchronous HTTP Fetcher utilizing httpx.AsyncClient for non-blocking network I/O.
    """

    def __init__(self, concurrency_limit: int = 5):
        self.concurrency_limit = concurrency_limit
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.client = httpx.AsyncClient(
            headers={"User-Agent": settings.USER_AGENT},
            timeout=httpx.Timeout(
                connect=10.0,
                read=float(settings.REQUEST_TIMEOUT),
                write=10.0,
                pool=10.0,
            ),
            follow_redirects=True,
        )

    async def fetch(self, url: str, retries: int = 3) -> Optional[str]:
        """
        Asynchronously fetch a page with semaphore concurrency control and retries.
        """
        async with self.semaphore:
            for attempt in range(1, retries + 1):
                logger.info(f"[Async] Attempt {attempt}/{retries} - Fetching {url}")
                try:
                    t0 = time.time()
                    response = await self.client.get(url)
                    response_time = time.time() - t0

                    logger.info(f"[Async] Status: {response.status_code} ({round(response_time, 2)}s)")
                    response.raise_for_status()
                    return response.text

                except httpx.TimeoutException:
                    logger.warning(f"[Async] Timeout for {url}")
                except httpx.HTTPStatusError as e:
                    logger.error(f"[Async] HTTP Error {e.response.status_code}: {e}")
                    # Only retry on 5xx server errors; stop on 4xx client errors
                    if e.response.status_code < 500:
                        break
                except httpx.RequestError as e:
                    logger.error(f"[Async] Network Error: {e}")
                except Exception as e:
                    logger.exception(f"[Async] Unexpected Error: {e}")
                    break

                if attempt < retries:
                    await asyncio.sleep(0.5 * attempt)

            return None

    async def close(self) -> None:
        """Close underlying HTTPX async client connection pool."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
