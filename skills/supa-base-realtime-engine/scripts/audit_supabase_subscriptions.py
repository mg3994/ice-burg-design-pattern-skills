#!/usr/bin/env python3
"""
audit_supabase_subscriptions.py
Audits Flutter presentation widgets for direct SupabaseClient references.
"""

import sys
from pathlib import Path

def audit_supabase(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    warnings = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        if "presentation" in dart_file.parts or "ui" in dart_file.parts:
            if "SupabaseClient" in content or ".stream(primaryKey:" in content:
                warnings.append(f"{rel_path}: Found direct Supabase reference in presentation layer! Move stream to Repository streamSignal.")

    print(f"--- Supabase Realtime Submersion Audit: {lib_dir} ---")
    if not warnings:
        print("✅ PASS: All Supabase stream channels properly submerged in repository.")
        sys.exit(0)

    print(f"⚠️ LEAK WARNINGS ({len(warnings)}):")
    for warn in warnings:
        print(f"  - {warn}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    audit_supabase(path_to_check)
