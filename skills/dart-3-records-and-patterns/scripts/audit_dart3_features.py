#!/usr/bin/env python3
"""
audit_dart3_features.py
Audits Dart source files for Dart 3 record usage and flags legacy class boilerplate.
"""

import sys
import re
from pathlib import Path

def audit_dart3(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    suggestions = []
    record_typedef_count = 0

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        # Count record typedefs
        records = re.findall(r'typedef\s+\w+\s*=\s*\(\{', content)
        record_typedef_count += len(records)

        # Check for legacy equatable / copyWith boilerplate
        if "extends Equatable" in content:
            suggestions.append(f"{rel_path}: Uses legacy Equatable class. Consider replacing with Dart 3 Records (`({ ... })`).")
        if "@freezed" in content:
            suggestions.append(f"{rel_path}: Uses @freezed code generation. Consider native Dart 3 records to eliminate build_runner.")

    print(f"--- Dart 3 Feature Audit for: {lib_dir} ---")
    print(f"Found {record_typedef_count} Pure Dart 3 Record definitions.")
    if not suggestions:
        print("✅ PASS: Codebase fully utilizes modern Dart 3 Records without legacy boilerplate.")
        sys.exit(0)

    print(f"💡 REFACTORING SUGGESTIONS ({len(suggestions)}):")
    for sug in suggestions:
        print(f"  - {sug}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    audit_dart3(path_to_check)
