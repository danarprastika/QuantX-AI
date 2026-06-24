#!/usr/bin/env python3
"""
Documentation dependency validation script.
Validates dependency graph and detects structural issues.
"""

import os
import re
import sys
from pathlib import Path
from typing import NamedTuple
from collections import defaultdict

DOCS_DIR = Path("docs")

TEMPLATE_HEADINGS = {"Overview", "Related Documents", "1. Purpose", "2. Scope"}
COMMON_HEADINGS = {"Architecture Overview", "Error Handling", "Monitoring", "Testing Strategy", 
                   "Performance Requirements", "Rate Limiting", "Incident Response", "State Management",
                   "Security Architecture", "Performance Optimization", "Logging Architecture", 
                   "Compliance", "API Versioning", "Message Queue Integration", "Reliability Patterns",
                   "Deployment Architecture", "Component Architecture", "Monitoring & Observability",
                   "Error Response Format", "Architectural Overview", "Architectural Overview"}


class DependencyError(NamedTuple):
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


def validate_dependencies() -> list[DependencyError]:
    """Check all markdown files for dependency issues."""
    errors = []
    all_docs = {f.name: f for f in DOCS_DIR.glob("*.md")}

    for md_file in DOCS_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        metadata = extract_yaml_front_matter(content)

        if not metadata:
            continue

        depends_on = metadata.get("depends_on", [])
        related_docs = metadata.get("related_documents", [])

        for dep in depends_on:
            if not isinstance(dep, str):
                continue
            dep_name = Path(dep).name
            if dep_name not in all_docs:
                errors.append(DependencyError(str(md_file), f"depends_on references non-existent file: {dep}"))
            if dep_name == md_file.name:
                errors.append(DependencyError(str(md_file), "depends_on references itself (self-reference)"))

        for rel in related_docs:
            if not isinstance(rel, str):
                continue
            rel_name = Path(rel).name
            if rel_name not in all_docs:
                errors.append(DependencyError(str(md_file), f"related_documents references non-existent file: {rel}"))

    return errors


def check_orphan_documents() -> list[DependencyError]:
    """Check for orphan documents (not referenced anywhere)."""
    errors = []
    all_docs = {f.name: f for f in DOCS_DIR.glob("*.md")}
    referenced = set()

    for md_file in DOCS_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")

        for match in re.finditer(r"\[.*?\]\(([^)]+\.md)\)", content):
            ref = Path(match.group(1)).name
            referenced.add(ref)

        metadata = extract_yaml_front_matter(content)
        if metadata:
            for dep in metadata.get("depends_on", []):
                if isinstance(dep, str):
                    referenced.add(Path(dep).name)
            for rel in metadata.get("related_documents", []):
                if isinstance(rel, str):
                    referenced.add(Path(rel).name)

    sot_matrix = DOCS_DIR / "SOURCE_OF_TRUTH.md"
    if sot_matrix.exists():
        matrix_content = sot_matrix.read_text(encoding="utf-8")
        for match in re.finditer(r"`([^`]+\.md)`", matrix_content):
            referenced.add(match.group(1))

    for doc in all_docs:
        if doc not in referenced and doc != "SOURCE_OF_TRUTH.md":
            governance_docs = {"DOCUMENTATION_RULES.md", "DOCUMENTATION_TEMPLATE.md",
                             "DOCUMENTATION_GOVERNANCE.md", "DOCUMENTATION_CHANGELOG.md",
                             "DOCUMENTATION_VALIDATION.md"}
            if doc not in governance_docs and doc != "INDEX.md":
                if doc not in referenced:
                    errors.append(DependencyError(doc, "Orphan document - not referenced in any related_documents or SOURCE_OF_TRUTH.md"))

    return errors


def check_duplicate_headings() -> list[DependencyError]:
    """Check for problematic duplicate H2 headings across documents - excluding template/common headings and code blocks."""
    errors = []
    heading_owners = {}

    for md_file in DOCS_DIR.glob("*.md"):
        if md_file.name in ("DOCUMENTATION_TEMPLATE.md",):
            continue
        content = md_file.read_text(encoding="utf-8")
        
        in_code_block = False
        for line in content.split("\n"):
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            
            match = re.match(r"^##\s+(.+)$", line)
            if match:
                heading = match.group(1).strip()
                if heading in TEMPLATE_HEADINGS or heading in COMMON_HEADINGS:
                    continue
                if heading in heading_owners:
                    errors.append(DependencyError(
                        str(md_file),
                        f"Duplicate H2 heading '{heading}' (also in {heading_owners[heading]})"
                    ))
                else:
                    heading_owners[heading] = str(md_file)

    return errors


def main() -> int:
    """Main entry point."""
    print("Checking dependencies...")

    dependency_errors = validate_dependencies()
    orphan_errors = check_orphan_documents()
    duplicate_errors = check_duplicate_headings()

    all_errors = dependency_errors + orphan_errors + duplicate_errors

    if all_errors:
        print(f"\nFound {len(all_errors)} dependency error(s):\n")
        for error in all_errors:
            print(f"  {error.file}: {error.error}")
        return 1

    print("All dependencies are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())