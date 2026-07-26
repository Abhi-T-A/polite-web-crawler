import argparse
import sys
from app.main import run_crawler


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Polite Scraper: A production-grade python web crawler."
    )

    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=None,
        help="Maximum number of pages to crawl.",
    )
    parser.add_argument(
        "--delay",
        "-d",
        type=float,
        default=None,
        help="Delay in seconds between requests.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Export scraped data to JSON format.",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Export scraped data to CSV format.",
    )
    parser.add_argument(
        "--sqlite",
        action="store_true",
        help="Persist scraped data into SQLite database.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose debug logging.",
    )

    return parser.parse_args(args)


def main():
    cli_args = parse_args()

    # Default to SQLite and JSON if no specific format flags are passed
    use_json = cli_args.json
    use_csv = cli_args.csv
    use_sqlite = cli_args.sqlite

    if not (use_json or use_csv or use_sqlite):
        use_sqlite = True
        use_json = True

    run_crawler(
        limit=cli_args.limit,
        delay=cli_args.delay,
        use_sqlite=use_sqlite,
        use_json=use_json,
        use_csv=use_csv,
        verbose=cli_args.verbose,
    )


if __name__ == "__main__":
    main()