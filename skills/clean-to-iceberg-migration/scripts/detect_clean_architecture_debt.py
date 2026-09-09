#!/usr/bin/env python3
"""
detect_clean_architecture_debt.py
Scans a Flutter project for Clean Architecture technical debt:
- Anemic Use Cases / Interactors
- StreamBuilder usage in UI
- Freezed / Equatable dependency overhead
"""

import sys
import re
from pathlib import Path

def detect_debt(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    debt_items = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        # 1. Anemic Use Cases
        if "domain/usecases" in dart_file.parts or "UseCase" in dart_file.name:
            if len(content.splitlines()) < 25:
                debt_items.append(f"{rel_path}: Anemic Use Case detected (< 25 lines). Consider removing and exposing repository signals directly.")

        # 2. StreamBuilder UI debt
        if "StreamBuilder" in content:
            debt_items.append(f"{rel_path}: Legacy StreamBuilder detected in UI layer. Submerge stream in Repository streamSignal.")

        # 3. Equatable / Freezed boilerplate
        if "extends Equatable" in content:
            debt_items.append(f"{rel_path}: Legacy Equatable detected. Migrate to pure Dart 3 Record typedef.")

    print(f"--- Clean Architecture Technical Debt Audit: {lib_dir} ---")
    if not debt_items:
        print("✅ PASS: Zero Clean Architecture debt detected.")
        sys.exit(0)

    print(f"⚠️ TECHNICAL DEBT DETECTED ({len(debt_items)}):")
    for item in debt_items:
        print(f"  - {item}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    detect_debt(path_to_check)
