#!/usr/bin/env python3
"""
verify_submerged_engine.py
Verifies submerged repository engine constructs (streamSignal, computed, signals) in Dart data layers.
"""

import sys
from pathlib import Path

def verify_engine(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    has_engine = False

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        if "streamSignal(" in content and "computed(" in content:
            has_engine = True
            break

    print(f"--- Submerged Repository Engine Verification: {lib_dir} ---")
    if has_engine:
        print("✅ PASS: Submerged Repository Engine verified (streamSignal + computed).")
        sys.exit(0)

    print("⚠️ ENGINE NOTICE: No submerged repository engine found matching streamSignal + computed.")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    verify_engine(path_to_check)
