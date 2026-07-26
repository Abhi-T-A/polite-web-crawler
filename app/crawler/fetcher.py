import time

import httpx

from app.config import settings
from app.utils.logger import logger


class Fetcher:
    """
    Responsible for downloading web pages.
    """

    def __init__(self):
        self.client = httpx.Client(
            headers={
                "User-Agent": settings.USER_AGENT,
            },
            timeout=httpx.Timeout(
                connect=10.0,
                read=settings.REQUEST_TIMEOUT,
                write=10.0,
                pool=10.0,
            ),
            follow_redirects=True,
        )

    def fetch(self, url: str, retries: int = 3) -> str | None:
        """
        Fetch HTML with retry support.
        """

        for attempt in range(1, retries + 1):
            logger.info(f"Attempt {attempt}/{retries} - Fetching {url}")

            try:
                response = self.client.get(url)

                logger.info(f"Status Code: {response.status_code}")

                response.raise_for_status()

                logger.info(f"Downloaded {len(response.text)} characters")

                return response.text

            except httpx.TimeoutException:
                logger.warning("Request timed out.")

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP Error: {e}")
                break

            except httpx.RequestError as e:
                logger.error(f"Network Error: {e}")

            except Exception as e:
                logger.exception(f"Unexpected Error: {e}")
                break

            if attempt < retries:
                logger.info("Retrying in 2 seconds...")
                time.sleep(2)

        return None

    def close(self):
        self.client.close()