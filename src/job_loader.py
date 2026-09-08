"""
Job data loader.

For now, jobs come from a local JSON file.
Later, this interface can be replaced with a real
job-search API or web-search adapter without changing
the evaluation layer.
"""

import json
from pathlib import Path


def load_jobs(path: str = "examples/jobs.json") -> list[dict]:
    """Load job opportunities from a JSON file."""

    file_path = Path(path)

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)
