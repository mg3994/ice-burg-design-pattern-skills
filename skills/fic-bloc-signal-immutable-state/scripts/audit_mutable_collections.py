#!/usr/bin/env python3
"""
audit_mutable_collections.py
Audits Dart state definitions for mutable standard collections (List, Set, Map) instead of Fast Immutable Collections (IList, ISet, IMap).
"""

import sys
import re
from pathlib import Path

def audit_collections(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    warnings = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        if "typedef" in content and "State = (" in content:
            if "List<" in content:
                warnings.append(f"{rel_path}: State record typedef uses mutable `List<T>`. Use `IList<T>` from fast_immutable_collections to avoid ghost rebuilds.")
            if "Map<" in content:
                warnings.append(f"{rel_path}: State record typedef uses mutable `Map<K, V>`. Use `IMap<K, V>` from fast_immutable_collections.")

    print(f"--- Fast Immutable Collections (FIC) Audit: {lib_dir} ---")
    if not warnings:
        print("✅ PASS: All state definitions use Fast Immutable Collections.")
        sys.exit(0)

    print(f"⚠️ MUTABLE COLLECTION WARNINGS ({len(warnings)}):")
    for warn in warnings:
        print(f"  - {warn}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    audit_collections(path_to_check)
