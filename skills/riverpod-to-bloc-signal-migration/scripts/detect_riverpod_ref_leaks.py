#!/usr/bin/env python3
"""
detect_riverpod_ref_leaks.py
Scans Flutter presentation widgets for legacy Riverpod ConsumerWidget / WidgetRef usages.
"""

import sys
from pathlib import Path

def detect_riverpod(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    items = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        if "ConsumerWidget" in content or "WidgetRef" in content or "StateNotifierProvider" in content:
            items.append(f"{rel_path}: Found legacy Riverpod reference! Migrate to CubitSignal and BlocBuilder.")

    print(f"--- Riverpod to BlocSignal Audit: {lib_dir} ---")
    if not items:
        print("✅ PASS: Zero legacy Riverpod dependencies detected.")
        sys.exit(0)

    print(f"💡 RIVERPOD DEBT DETECTED ({len(items)}):")
    for item in items:
        print(f"  - {item}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    detect_riverpod(path_to_check)
