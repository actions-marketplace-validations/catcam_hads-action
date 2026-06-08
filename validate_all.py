#!/usr/bin/env python3
"""
HADS Validator — batch runner for GitHub Actions.

Usage:
    python validate_all.py [glob_pattern] [fail_on_violation]

Arguments:
    glob_pattern      Glob pattern for .md files (default: **/*.md)
    fail_on_violation Exit 1 on violations if 'true' (default: true)
"""

import glob
import os
import sys

# Allow importing validate.py from the same directory as this script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import validate

SKIP_DIRS = {"node_modules", "venv", ".git"}


def should_skip(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    return any(part in SKIP_DIRS for part in parts)


def main() -> int:
    pattern = sys.argv[1] if len(sys.argv) > 1 else "**/*.md"
    fail_on_violation = sys.argv[2].strip().lower() if len(sys.argv) > 2 else "true"

    files = glob.glob(pattern, recursive=True)
    files = [f for f in files if not should_skip(f)]

    if not files:
        print(f"No .md files found matching pattern: {pattern}")
        return 0

    total = len(files)
    valid_count = 0
    invalid_files = []

    for path in sorted(files):
        result = validate(path)
        if result == 0:
            valid_count += 1
        else:
            invalid_files.append(path)

    print("\n" + "=" * 60)
    print(f"HADS Validation Summary: {valid_count}/{total} files valid")

    if invalid_files:
        print(f"\nInvalid files ({len(invalid_files)}):")
        for f in invalid_files:
            print(f"  - {f}")

    print("=" * 60)

    if invalid_files and fail_on_violation == "true":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
