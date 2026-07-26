from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


class URLManager:
    """
    Manages visited URLs, normalizes URLs to canonical forms,
    and prevents duplicate crawling.
    """

    def __init__(self):
        self.visited_urls: set[str] = set()

    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalizes a URL to its canonical form:
        - Converts scheme and host to lowercase
        - Removes URL fragments (#...)
        - Sorts query parameters
        - Strips trailing slashes from path (except root '/')
        """
        if not url:
            return ""

        parsed = urlparse(url.strip())
        
        # Lowercase scheme and netloc
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        
        # Normalize path
        path = parsed.path
        if len(path) > 1 and path.endswith("/"):
            path = path.rstrip("/")

        # Sort query parameters
        query_params = parse_qsl(parsed.query, keep_blank_values=True)
        sorted_query = urlencode(sorted(query_params))

        # Omit fragment
        canonical_tuple = (scheme, netloc, path, parsed.params, sorted_query, "")
        return urlunparse(canonical_tuple)

    def is_visited(self, url: str) -> bool:
        """Check if a URL has already been visited."""
        canonical = self.normalize_url(url)
        return canonical in self.visited_urls

    def add_visited(self, url: str) -> bool:
        """
        Add a URL to the visited set.
        Returns True if the URL was new, or False if it was already visited.
        """
        canonical = self.normalize_url(url)
        if canonical in self.visited_urls:
            return False
        self.visited_urls.add(canonical)
        return True

    def reset(self) -> None:
        """Clear all visited URLs."""
        self.visited_urls.clear()

    @property
    def visited_count(self) -> int:
        """Returns total number of unique visited URLs."""
        return len(self.visited_urls)
