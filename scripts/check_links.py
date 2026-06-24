#!/usr/bin/env python3
"""
Documentation link validation script.
Detects broken markdown links and invalid internal references.
"""

import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

DOCS_DIR = Path("docs")

TEMPLATE_FILES = {"DOCUMENTATION_TEMPLATE.md", "DOCUMENTATION_RULES.md", "DOCUMENTATION_VALIDATION.md"}


class BrokenLink(NamedTuple):
    file: str
    line: int
    link: str
    error: str


def extract_markdown_links(content: str) -> list[tuple[int, str, str]]:
    """Extract all markdown links with line numbers."""
    links = []
    for i, line in enumerate(content.split("\n"), 1):
        for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
            links.append((i, match.group(1), match.group(2)))
    return links


def validate_internal_link(link_target: str, source_file: Path) -> str | None:
    """Validate that an internal link resolves to an existing file."""
    if link_target.startswith(("http://", "https://", "mailto:", "#", "javascript:")):
        return None
    if link_target.startswith("/docs/"):
        return None
    if link_target in ("XX_FILENAME.md", "YY_FILENAME.md", "XX_DOCUMENT_NAME.md"):
        return None
    if re.match(r"^[A-Z_]+$", link_target) or link_target in ("url", "path"):
        return None

    target_path = (source_file.parent / link_target).resolve()
    if not target_path.exists():
        return f"File does not exist: {link_target}"

    return None


def validate_heading_link(content: str, link_target: str, line_no: int) -> str | None:
    """Validate that heading anchors exist in the same document."""
    if not link_target.startswith("#"):
        return None

    anchor = link_target[1:]
    heading_pattern = rf"^#+\s+{re.escape(anchor)}\b"
    if not re.search(heading_pattern, content, re.MULTILINE):
        return f"Heading anchor #{anchor} not found"
    return None


def check_broken_links() -> list[BrokenLink]:
    """Check all markdown files for broken links."""
    broken_links = []

    for md_file in DOCS_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        for line_no, text, link in extract_markdown_links(content):
            if link.startswith(("http://", "https://", "mailto:")):
                continue

            error = validate_internal_link(link, md_file)
            if error:
                broken_links.append(BrokenLink(str(md_file), line_no, link, error))
            elif link.startswith("#"):
                error = validate_heading_link(content, link, line_no)
                if error:
                    broken_links.append(BrokenLink(str(md_file), line_no, link, error))

    return broken_links


def main() -> int:
    """Main entry point."""
    print("Checking for broken links...")
    broken_links = check_broken_links()

    if broken_links:
        print(f"\nFound {len(broken_links)} broken link(s):\n")
        for link in broken_links:
            print(f"  {link.file}:{link.line}: [{link.link}] - {link.error}")
        return 1

    print("All links are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())