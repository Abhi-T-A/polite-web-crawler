import time

from app.config import settings
from app.utils.logger import logger


class RateLimiter:
    """
    Controls the request rate.
    """

    @staticmethod
    def wait():

        logger.info(
            f"Sleeping for {settings.REQUEST_DELAY} seconds..."
        )

        time.sleep(settings.REQUEST_DELAY)