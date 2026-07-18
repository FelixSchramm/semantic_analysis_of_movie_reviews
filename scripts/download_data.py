"""Download the movie-review dataset (``MovieReview.csv``).

The 32 MB dataset is hosted as a GitHub release asset instead of being committed
to the repository, so clones stay small. Run this once from the repo root:

    python scripts/download_data.py

Set ``DATA_URL`` (or the ``MOVIEREVIEW_DATA_URL`` environment variable) if you
host the file somewhere else.
"""

from __future__ import annotations

import os
import sys
import urllib.request
from pathlib import Path

DATA_URL = os.environ.get(
    "MOVIEREVIEW_DATA_URL",
    "https://github.com/FelixSchramm/semantic_analysis_of_movie_reviews/"
    "releases/download/dataset-v1/MovieReview.csv",
)
DEST = Path("MovieReview.csv")


def main() -> int:
    if DEST.exists():
        print(f"{DEST} already exists; nothing to do.")
        return 0
    print(f"Downloading {DATA_URL}\n     -> {DEST} ...")
    try:
        urllib.request.urlretrieve(DATA_URL, DEST)
    except Exception as exc:  # noqa: BLE001 - surface any download failure clearly
        print(f"Download failed: {exc}", file=sys.stderr)
        print(
            "Set MOVIEREVIEW_DATA_URL to a reachable URL if the release asset "
            "is not available.",
            file=sys.stderr,
        )
        return 1
    print(f"Done ({DEST.stat().st_size / 1e6:.1f} MB).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
