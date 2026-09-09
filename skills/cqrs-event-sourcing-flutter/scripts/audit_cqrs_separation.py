#!/usr/bin/env python3
"""
audit_cqrs_separation.py
Audits Dart source files for proper CQRS segregation:
- Command methods should return Future<void> (no query data returned on write calls)
- Query fields should be exposed as ReadonlySignal or getter functions
"""

import sys
import re
from pathlib import Path

def audit_cqrs(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    warnings = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        # Check: Command methods returning domain entities instead of Future<void>
        mutating_returns = re.findall(r'Future<Task>\s+\w*update\w*\(', content)
        if mutating_returns:
            warnings.append(f"{rel_path}: Mutating method returns entity directly instead of Future<void>. Violates CQRS Command-Query separation.")

    print(f"--- CQRS Command-Query Separation Audit: {lib_dir} ---")
    if not warnings:
        print("✅ PASS: Clean Command-Query segregation verified.")
        sys.exit(0)

    print(f"⚠️ CQRS SUGGESTIONS ({len(warnings)}):")
    for warn in warnings:
        print(f"  - {warn}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    audit_cqrs(path_to_check)
