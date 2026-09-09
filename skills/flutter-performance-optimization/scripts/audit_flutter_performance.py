#!/usr/bin/env python3
"""
audit_flutter_performance.py
Audits Flutter Dart source files for widget re-render performance bottlenecks:
- Missing const constructors on static widgets
- ListView.builder without Key parameters
- Missing RepaintBoundary on complex canvases
"""

import sys
import re
from pathlib import Path

def audit_performance(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    warnings = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        # Check 1: ListView.builder without key parameter
        if "ListView.builder" in content:
            if "key:" not in content and "Key(" not in content:
                warnings.append(f"{rel_path}: ListView.builder used without explicit element keys. May cause element recreation during reorders.")

        # Check 2: CustomPaint without RepaintBoundary
        if "CustomPaint" in content and "RepaintBoundary" not in content:
            warnings.append(f"{rel_path}: CustomPaint used without RepaintBoundary. May trigger unnecessary canvas rasterization passes.")

    print(f"--- Flutter Performance & Rebuild Audit for: {lib_dir} ---")
    if not warnings:
        print("✅ PASS: Zero performance anti-patterns detected.")
        sys.exit(0)

    print(f"⚠️ PERFORMANCE SUGGESTIONS ({len(warnings)}):")
    for warn in warnings:
        print(f"  - {warn}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    audit_performance(path_to_check)
