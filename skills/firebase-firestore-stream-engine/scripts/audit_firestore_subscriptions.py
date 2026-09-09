#!/usr/bin/env python3
"""
audit_firestore_subscriptions.py
Audits Flutter presentation widgets for direct FirebaseFirestore / StreamBuilder references.
"""

import sys
from pathlib import Path

def audit_firestore(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    warnings = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        if "presentation" in dart_file.parts or "ui" in dart_file.parts:
            if "FirebaseFirestore" in content or ".snapshots()" in content:
                warnings.append(f"{rel_path}: Found direct Firestore reference in presentation layer! Move to Repository streamSignal.")

    print(f"--- Firestore Stream Submersion Audit: {lib_dir} ---")
    if not warnings:
        print("✅ PASS: All Firestore snapshot streams properly submerged in repository.")
        sys.exit(0)

    print(f"⚠️ LEAK WARNINGS ({len(warnings)}):")
    for warn in warnings:
        print(f"  - {warn}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    audit_firestore(path_to_check)
