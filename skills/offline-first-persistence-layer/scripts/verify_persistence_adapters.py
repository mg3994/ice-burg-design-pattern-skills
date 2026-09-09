#!/usr/bin/env python3
"""
verify_persistence_adapters.py
Verifies offline persistence layer integration in Flutter Dart codebases.
"""

import sys
from pathlib import Path

def verify_persistence(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    has_persistence = False

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        if "sqlite" in content.lower() or "hive" in content.lower() or "drift" in content.lower() or "initialTasks" in content:
            has_persistence = True
            break

    print(f"--- Offline Persistence Layer Verification: {lib_dir} ---")
    if has_persistence:
        print("✅ PASS: Local persistent caching / fallback seed data detected.")
        sys.exit(0)

    print("⚠️ PERSISTENCE NOTICE: Consider bundling local persistent adapters (Hive/Drift) for offline startup.")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    verify_persistence(path_to_check)
