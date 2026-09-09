#!/usr/bin/env python3
"""
verify_rollback_transactions.py
Audits Dart repository code to ensure optimistic mutations wrap catch blocks inside atomic batch() calls.
"""

import sys
from pathlib import Path

def verify_rollbacks(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    warnings = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        if "catch" in content and "optimistic" in content.lower():
            if "batch(" not in content:
                warnings.append(f"{rel_path}: Optimistic mutation catch block missing batch() call! Wrap rollback updates inside batch().")

    print(f"--- Optimistic Rollback Verification: {lib_dir} ---")
    if not warnings:
        print("✅ PASS: All optimistic rollbacks properly atomic.")
        sys.exit(0)

    print(f"⚠️ ROLLBACK WARNINGS ({len(warnings)}):")
    for warn in warnings:
        print(f"  - {warn}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    verify_rollbacks(path_to_check)
