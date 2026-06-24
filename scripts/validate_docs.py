#!/usr/bin/env python3
"""
Main documentation validation script.
Orchestrates all validation checks and reports results.
"""

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def run_check(script_name: str) -> int:
    """Run a validation script and return its exit code."""
    script_path = SCRIPTS_DIR / script_name
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=False,
        text=True
    )
    return result.returncode


def main() -> int:
    """Run all validation checks."""
    print("=" * 60)
    print("QuantX AI Documentation Validation")
    print("=" * 60)
    print()

    checks = [
        ("check_metadata.py", "Metadata Validation"),
        ("check_links.py", "Link Validation"),
        ("check_source_of_truth.py", "Source of Truth Validation"),
        ("check_dependencies.py", "Dependency Validation"),
    ]

    failures = 0
    for script, name in checks:
        print(f"\n--- {name} ---")
        if run_check(script) != 0:
            failures += 1
        print()

    print("=" * 60)
    if failures:
        print(f"VALIDATION FAILED: {failures} check(s) failed")
        return 1
    print("VALIDATION PASSED: All checks successful")
    return 0


if __name__ == "__main__":
    sys.exit(main())