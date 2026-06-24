#!/usr/bin/env python3
"""
Documentation metadata validation script.
Validates YAML front matter and required fields.
"""

import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

DOCS_DIR = Path("docs")

REQUIRED_FIELDS = ["status", "owner", "version", "last_updated", "source_of_truth", "depends_on", "related_documents"]
VALID_STATUSES = ["Draft", "In Review", "Approved", "Deprecated", "Archived"]


class MetadataError(NamedTuple):
    file: str
    error: str


def extract_yaml_front_matter(content: str) -> tuple[dict | None, str | None]:
    """Extract YAML front matter from markdown content."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None, "Missing YAML front matter"

    yaml_content = match.group(1)
    try:
        import yaml
        data = yaml.safe_load(yaml_content)
        return data, None
    except yaml.YAMLError as e:
        return None, f"Invalid YAML: {e}"


def validate_version(version: str) -> str | None:
    """Validate semantic versioning format."""
    if not re.match(r"^\d+\.\d+\.\d+$", str(version)):
        return f"Invalid version format: {version} (expected MAJOR.MINOR.PATCH)"
    return None


def validate_date(date_str: str) -> str | None:
    """Validate ISO 8601 date format."""
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(date_str)):
        return f"Invalid date format: {date_str} (expected YYYY-MM-DD)"
    return None


def validate_status(status: str) -> str | None:
    """Validate status value."""
    if status not in VALID_STATUSES:
        return f"Invalid status: {status} (expected one of {VALID_STATUSES})"
    return None


def validate_metadata() -> list[MetadataError]:
    """Check all markdown files for metadata issues."""
    errors = []

    for md_file in DOCS_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        metadata, error = extract_yaml_front_matter(content)

        if error:
            errors.append(MetadataError(str(md_file), error))
            continue

        for field in REQUIRED_FIELDS:
            if field not in metadata:
                errors.append(MetadataError(str(md_file), f"Missing required field: {field}"))

        if "version" in metadata and metadata["version"]:
            error = validate_version(metadata["version"])
            if error:
                errors.append(MetadataError(str(md_file), error))

        if "last_updated" in metadata and metadata["last_updated"]:
            error = validate_date(metadata["last_updated"])
            if error:
                errors.append(MetadataError(str(md_file), error))

        if "status" in metadata and metadata["status"]:
            error = validate_status(metadata["status"])
            if error:
                errors.append(MetadataError(str(md_file), error))

    return errors


def main() -> int:
    """Main entry point."""
    print("Checking metadata...")
    errors = validate_metadata()

    if errors:
        print(f"\nFound {len(errors)} metadata error(s):\n")
        for error in errors:
            print(f"  {error.file}: {error.error}")
        return 1

    print("All metadata is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())