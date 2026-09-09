#!/usr/bin/env python3
"""
audit_monorepo_dependencies.py
Audits monorepo package structures to verify pure Dart domain/data packages do not depend on package:flutter.
"""

import sys
from pathlib import Path

def audit_monorepo(workspace_dir="."):
    workspace_path = Path(workspace_dir)
    if not workspace_path.exists():
        print(f"Error: Path {workspace_dir} does not exist.")
        sys.exit(1)

    violations = []

    for pubspec in workspace_path.rglob("pubspec.yaml"):
        # Ignore root pubspec if checking packages
        if "packages" in pubspec.parts or "domain" in pubspec.name or "data" in pubspec.name:
            content = pubspec.read_text(encoding="utf-8")
            rel_path = pubspec.relative_to(workspace_path)

            if "domain" in str(pubspec).lower() or "data" in str(pubspec).lower():
                if "sdk: flutter" in content:
                    violations.append(f"{rel_path}: Pure Dart domain/data package contains `sdk: flutter` dependency! Keep domain/data pure Dart.")

    print(f"--- Monorepo Package Layering Audit: {workspace_dir} ---")
    if not violations:
        print("✅ PASS: Domain and Data packages maintain pure Dart independence.")
        sys.exit(0)

    print(f"❌ LAYER VIOLATIONS ({len(violations)}):")
    for v in violations:
        print(f"  - {v}")
    sys.exit(1)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "."
    audit_monorepo(path_to_check)
