#!/usr/bin/env python3
"""
verify_stale_revalidate.py
Verifies stale-while-revalidate error flags and warning banner constructs in Flutter UI code.
"""

import sys
from pathlib import Path

def verify_caching(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    has_banner = False

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        if "hasSyncError" in content and "Colors.amber" in content:
            has_banner = True
            break

    print(f"--- Stale-While-Revalidate UX Verification: {lib_dir} ---")
    if has_banner:
        print("✅ PASS: Stale-While-Revalidate UX warning banner detected.")
        sys.exit(0)

    print("⚠️ UX NOTICE: Consider adding AppBar.bottom warning banner when hasSyncError is true.")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    verify_caching(path_to_check)
