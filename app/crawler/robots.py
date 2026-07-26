from urllib import robotparser

from app.utils.logger import logger


class RobotsChecker:

    def __init__(self, user_agent: str):

        self.user_agent = user_agent

        self.parser = robotparser.RobotFileParser()

    def load(self, base_url: str):

        robots_url = base_url.rstrip("/") + "/robots.txt"

        logger.info(f"Loading robots.txt: {robots_url}")

        self.parser.set_url(robots_url)

        self.parser.read()

    def can_fetch(self, url: str) -> bool:

        allowed = self.parser.can_fetch(
            self.user_agent,
            url
        )

        if allowed:
            logger.info(f"Allowed: {url}")
        else:
            logger.warning(f"Blocked by robots.txt: {url}")

        return allowed