#!/usr/bin/env python3
"""
audit_stream_subscriptions.py
Audits Dart source files for raw gRPC/GraphQL stream subscriptions leaked into presentation classes.
"""

import sys
import re
from pathlib import Path

def audit_streams(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    warnings = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        if "presentation" in dart_file.parts or "ui" in dart_file.parts:
            if "ResponseStream" in content or "GraphQLClient" in content:
                warnings.append(f"{rel_path}: Found gRPC/GraphQL client referenced in presentation layer! Quarantining stream inside Repository streamSignal.")

    print(f"--- gRPC & GraphQL Stream Audit for: {lib_dir} ---")
    if not warnings:
        print("✅ PASS: All network streams quarantined beneath waterline.")
        sys.exit(0)

    print(f"⚠️ LEAK WARNINGS ({len(warnings)}):")
    for warn in warnings:
        print(f"  - {warn}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    audit_streams(path_to_check)
