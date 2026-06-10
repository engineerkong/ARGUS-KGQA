"""Client for the ARGUS readings API."""

import requests
from typing import Iterator, Optional

BASE_URL = "http://api.argusservices.athenarc.gr/api/readings"


def fetch_page(page: int = 1, **params) -> dict:
    """Fetch a single page of readings. Returns the raw JSON response."""
    response = requests.get(BASE_URL, params={"page": page, **params}, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_readings(max_pages: Optional[int] = None, **params) -> Iterator[dict]:
    """Yield individual reading records across all pages (or up to max_pages)."""
    page = 1
    while True:
        data = fetch_page(page, **params)
        yield from data["data"]
        meta = data["meta"]
        if page >= meta["last_page"]:
            break
        if max_pages is not None and page >= max_pages:
            break
        page += 1


def fetch_all(max_pages: Optional[int] = None, **params) -> list[dict]:
    """Return all reading records as a list."""
    return list(fetch_readings(max_pages=max_pages, **params))

if __name__ == "__main__":
    records = fetch_all(max_pages=1)  # Example: fetch first 1 pages of readings
    print(f"Fetched {len(records)} records:")
    for record in records:
        print(record)