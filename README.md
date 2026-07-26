# Polite Web Scraper 🕷️

A pythonic web crawler built to scrape e-commerce data from [books.toscrape.com](https://books.toscrape.com).

This repository implements a **polite scraping pipeline** that respects site rules (`robots.txt`), throttles requests using rate limiting, cleans extracted fields, validates data schemas, and persists structured records.

---

## 🔄 Scraping Pipeline

```text
Fetch (HTTPX)
  ↓
Parse (BeautifulSoup + lxml)
  ↓
Extract (DOM selector parsing)
  ↓
Clean (Currency & rating normalization)
  ↓
Structure (Pydantic BookRecord schemas)
  ↓
Save (SQLite database & JSON export)
```

---

## ✨ Key Features

- **Politeness First**: Checks `robots.txt` before fetching and enforces configurable delays (`REQUEST_DELAY=2s`).
- **Data Validation**: Uses Pydantic (`BookRecord`) to guarantee type-safe titles, prices, ratings, and URLs.
- **Deduplication**: `URLManager` tracks visited links and canonical URLs to prevent infinite crawl loops.
- **Dual Persistence**: Stores records in **SQLite** (`scraper.db` with `UNIQUE` constraint) and exports to **JSON** (`data.json`).
- **Structured Logging**: Log messages saved to `logs/scraper.log`.

---

## 📁 Project Layout

```text
polite_scraper/
├── app/
│   ├── crawler/
│   │   ├── fetcher.py     # HTTP Client with retries
│   │   ├── limiter.py     # Rate limiting delay
│   │   ├── robots.py      # Robots.txt validator
│   │   ├── scheduler.py   # Next-page pagination
│   │   └── url_manager.py # URL normalization & visited tracking
│   ├── models/
│   │   └── record.py      # Pydantic data schema
│   ├── parser/
│   │   ├── html_parser.py # BeautifulSoup HTML parser
│   │   ├── extractor.py   # DOM extraction
│   │   └── cleaner.py     # Price & rating cleaner
│   ├── storage/
│   │   ├── sqlite_storage.py # SQLite database export
│   │   └── json_storage.py   # JSON file export
│   ├── utils/
│   │   ├── logger.py      # Logging setup
│   │   └── stats.py       # Metrics collector
│   └── main.py            # Main pipeline execution loop
├── logs/                  # Application logs
├── app/output/            # Output data files (scraper.db, data.json)
├── run.py                 # Application entrypoint
├── requirements.txt       # Project dependencies
├── .env.example           # Environment variables template
└── README.md              # Documentation
```

---

## 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

3. **Execute Crawler**:
   ```bash
   python run.py
   ```

4. **Run Unit Tests**:
   ```bash
   pytest tests/
   ```
