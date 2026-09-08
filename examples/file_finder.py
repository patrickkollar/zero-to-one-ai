#!/usr/bin/env python3
"""Simple file finder utility.

Examples:
    python run_finder.py .
    python run_finder.py "C:\\Projects" --name "*.py"
    python run_finder.py . --contains "TODO" --max-depth 2
"""

from __future__ import annotations

import argparse
import fnmatch
import os
from pathlib import Path
from typing import Iterable, List, Sequence


def _iter_files(root: Path, *, include_hidden: bool = False, max_depth: int | None = None) -> Iterable[Path]:
    """Yield files under root, optionally limiting depth."""
    root = root.resolve()
    if not root.exists():
        return []

    def walk(current: Path, depth: int = 0):
        try:
            entries = sorted(current.iterdir(), key=lambda p: p.name.lower())
        except OSError:
            return

        for entry in entries:
            if not include_hidden and entry.name.startswith("."):
                continue

            if entry.is_dir():
                if max_depth is not None and depth >= max_depth:
                    continue
                yield from walk(entry, depth + 1)
            else:
                yield entry

    return walk(root)


def find_files(
    root: str | os.PathLike[str],
    name: str | None = None,
    pattern: str | None = None,
    contains: str | None = None,
    extension: str | None = None,
    include_hidden: bool = False,
    max_depth: int | None = None,
) -> List[str]:
    """Return matching file paths relative to root when possible.

    Args:
        root: Directory to search.
        name: Simple filename or substring match.
        pattern: Glob pattern like "*.py" or "**/*.txt".
        contains: Text to search inside file contents.
        extension: File extension to match (e.g., ".py").
        include_hidden: Include hidden files/directories.
        max_depth: Maximum directory depth from the root.
    """
    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(f"Directory not found: {root}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    matches: List[str] = []
    for file_path in _iter_files(root_path, include_hidden=include_hidden, max_depth=max_depth):
        try:
            relative = file_path.relative_to(root_path)
            display = relative.as_posix()
        except ValueError:
            display = file_path.as_posix()

        file_name = file_path.name

        if name:
            needle = name.lower()
            if needle not in file_name.lower() and needle not in display.lower():
                continue

        if pattern:
            if not fnmatch.fnmatch(display, pattern) and not fnmatch.fnmatch(file_name, pattern):
                continue

        if extension:
            normalized = extension if extension.startswith(".") else f".{extension}"
            if file_path.suffix.lower() != normalized.lower():
                continue

        if contains is not None:
            try:
                with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
                    content = handle.read()
            except (OSError, UnicodeDecodeError):
                continue
            if contains not in content:
                continue

        matches.append(display)

    return matches


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Find files in a directory tree.")
    parser.add_argument("root", nargs="?", default=".", help="Directory to search from (default: current directory).")
    parser.add_argument("--name", help="Match file names containing this text.")
    parser.add_argument("--pattern", help="Glob pattern to match against the path or file name, e.g. '*.py'.")
    parser.add_argument("--contains", help="Only include files whose contents contain this text.")
    parser.add_argument("--extension", help="Only include files with this extension (for example: .py or py).")
    parser.add_argument("--hidden", action="store_true", help="Include hidden files and directories.")
    parser.add_argument("--max-depth", type=int, default=None, help="Maximum number of subdirectories to descend.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        matches = find_files(
            root=args.root,
            name=args.name,
            pattern=args.pattern,
            contains=args.contains,
            extension=args.extension,
            include_hidden=args.hidden,
            max_depth=args.max_depth,
        )
    except (FileNotFoundError, NotADirectoryError) as exc:
        parser.error(str(exc))

    if not matches:
        print("No files found.")
        return 0

    for match in matches:
        print(match)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
