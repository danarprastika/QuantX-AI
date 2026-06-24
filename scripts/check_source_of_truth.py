#!/usr/bin/env python3
"""
Source of Truth validation script.
Validates that source_of_truth references are correct and consistent.
"""

import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

DOCS_DIR = Path("docs")


class SoTError(NamedTuple):
    file: str
    error: str


def extract_yaml_front_matter(content: str) -> dict | None:
    """Extract YAML front matter from markdown content."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None

    try:
        import yaml
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def validate_source_of_truth() -> list[SoTError]:
    """Check all markdown files for source of truth issues."""
    errors = []
    source_of_truth_files = set()

    for md_file in DOCS_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        metadata = extract_yaml_front_matter(content)

        if not metadata:
            continue

        file_stem = md_file.name
        sot = metadata.get("source_of_truth", "")

        if sot:
            sot_path = Path(sot)
            if not sot_path.exists():
                errors.append(SoTError(str(md_file), f"source_of_truth file does not exist: {sot}"))
            elif sot_path.name != file_stem:
                errors.append(SoTError(
                    str(md_file),
                    f"source_of_truth mismatch: file is {file_stem}, but metadata says {sot_path.name}"
                ))
            source_of_truth_files.add(sot_path.name)
        else:
            errors.append(SoTError(str(md_file), "Missing source_of_truth field"))

    sot_matrix = DOCS_DIR / "SOURCE_OF_TRUTH.md"
    if sot_matrix.exists():
        matrix_content = sot_matrix.read_text(encoding="utf-8")
        referenced_in_matrix = set(re.findall(r"`(\d{2}_[A-Z_]+\.md|DOCUMENTATION_[A-Z_]+\.md)`", matrix_content))
        document_files = {f.name for f in DOCS_DIR.glob("*.md")}

        for doc in document_files:
            if doc not in referenced_in_matrix and doc != "SOURCE_OF_TRUTH.md":
                if doc.startswith(("01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_", "10_",
                                   "11_", "12_", "13_", "14_", "15_", "16_", "17_", "18_", "19_",
                                   "20_", "21_", "22_", "23_", "24_", "25_", "26_", "27_", "28_",
                                   "29_", "30_", "31_", "32_", "33_", "34_", "35_", "36_", "37_",
                                   "38_", "39_", "40_", "41_", "42_", "43_", "44_", "45_", "46_",
                                   "47_", "48_", "49_", "50_", "51_", "52_", "53_", "54_", "55_",
                                   "56_", "57_", "58_", "59_", "60_")):
                    if doc not in source_of_truth_files:
                        errors.append(SoTError(doc, "Document not listed in SOURCE_OF_TRUTH.md matrix"))

    return errors


def main() -> int:
    """Main entry point."""
    print("Checking source of truth references...")
    errors = validate_source_of_truth()

    if errors:
        print(f"\nFound {len(errors)} source of truth error(s):\n")
        for error in errors:
            print(f"  {error.file}: {error.error}")
        return 1

    print("All source of truth references are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())