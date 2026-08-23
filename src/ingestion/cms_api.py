"""CMS data ingestion utilities.

The client is intentionally small and testable. Dataset-specific endpoint
configuration will be added as the production source is wired in.
"""

from pathlib import Path

import requests

CMS_BASE_URL = "https://data.cms.gov/provider-data/api/1"


def download_json(url: str, destination: Path, timeout: int = 60) -> Path:
    """Download a JSON response to a local raw-data file."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(response.text, encoding="utf-8")
    return destination


def main() -> None:
    print("CMS ingestion client ready. Dataset endpoint configuration is next.")


if __name__ == "__main__":
    main()
