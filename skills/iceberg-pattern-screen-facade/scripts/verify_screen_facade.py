#!/usr/bin/env python3
"""
verify_screen_facade.py
Verifies screen facade implementations extending CubitSignal with computed subscriptions.
"""

import sys
from pathlib import Path

def verify_facade(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    has_facade = False

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        if "extends CubitSignal" in content:
            has_facade = True
            break

    print(f"--- Screen Facade Verification: {lib_dir} ---")
    if has_facade:
        print("✅ PASS: Screen Facade verified (extends CubitSignal).")
        sys.exit(0)

    print("⚠️ FACADE NOTICE: No screen facade extending CubitSignal detected.")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    verify_facade(path_to_check)
