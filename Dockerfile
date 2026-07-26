# Production Multi-Stage Dockerfile for Polite Scraper
FROM python:3.12-slim AS builder

WORKDIR /app

# Prevent Python from writing bytecode and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final runtime image
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source code
COPY . .

# Ensure volume mount directories exist
RUN mkdir -p app/output logs

# Default command runs CLI crawler
ENTRYPOINT ["python", "run.py"]
CMD ["--limit", "5"]
