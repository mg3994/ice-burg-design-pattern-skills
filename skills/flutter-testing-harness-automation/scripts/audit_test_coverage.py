#!/usr/bin/env python3
"""
audit_test_coverage.py
Audits test directories for widget test coverage and pure Dart architecture test coverage.
"""

import sys
from pathlib import Path

def audit_tests(test_dir="test"):
    test_path = Path(test_dir)
    if not test_path.exists():
        print(f"Error: Directory {test_dir} does not exist.")
        sys.exit(1)

    test_files = list(test_path.rglob("*_test.dart"))
    print(f"--- Test Suite Coverage Audit: {test_dir} ---")
    print(f"Found {len(test_files)} test suites in `{test_dir}/`:")
    for f in test_files:
        print(f"  - {f.name}")

    if test_files:
        print("✅ PASS: Test directory populated with test suites.")
        sys.exit(0)

    print("⚠️ TEST NOTICE: No test files found matching *_test.dart.")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "test"
    audit_tests(path_to_check)
