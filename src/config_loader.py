"""
Configuration loader.

Loads the candidate profile and scoring model from YAML files.
Keeping configuration outside the Python code makes the system
easier to adapt without changing the reasoning or workflow.
"""

from pathlib import Path

import yaml


def load_yaml(path: str) -> dict:
    """Load a YAML configuration file."""

    file_path = Path(path)

    with file_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)