#!/usr/bin/env python3
"""
validate_iceberg_architecture.py
Analyzes Dart source files in a project for Iceberg Pattern architectural compliance.
Checks for anti-patterns:
- StreamBuilder or FutureBuilder in presentation layer
- Flutter framework imports in domain model layer
- Missing batch() calls in repository exception/rollback handling
"""

import sys
import re
from pathlib import Path

def analyze_project(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    errors = []
    warnings = []

    for dart_file in lib_path.rglob("*.dart"):
        rel_path = dart_file.relative_to(lib_path)
        content = dart_file.read_text(encoding="utf-8")

        # Check 1: Presentation layer anti-patterns
        if "presentation" in dart_file.parts or "ui" in dart_file.parts:
            if "StreamBuilder" in content:
                errors.append(f"{rel_path}: Found StreamBuilder in presentation layer! Iceberg Pattern requires synchronous state projection via BlocBuilder/SignalBuilder.")
            if "FutureBuilder" in content:
                errors.append(f"{rel_path}: Found FutureBuilder in presentation layer! Quarantined repository signals should provide sync values.")

        # Check 2: Domain layer purity
        if "domain" in dart_file.parts:
            if "package:flutter/material.dart" in content or "package:flutter/widgets.dart" in content:
                errors.append(f"{rel_path}: Domain layer imports Flutter UI packages! Domain layer must be pure Dart 3.")

        # Check 3: Repository optimistic rollback batching
        if "data" in dart_file.parts or "repository" in dart_file.name:
            if "catch" in content and "batch(" not in content:
                warnings.append(f"{rel_path}: Repository contains catch blocks without batch() calls. Ensure atomic state updates during optimistic rollbacks.")

    print(f"--- Iceberg Pattern Architectural Verification for: {lib_dir} ---")
    if not errors and not warnings:
        print("✅ PASS: Architectural rules satisfied. Zero stream leaks or domain dependencies found.")
        sys.exit(0)

    if errors:
        print(f"❌ ERRORS FOUND ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")

    if warnings:
        print(f"⚠️ WARNINGS ({len(warnings)}):")
        for warn in warnings:
            print(f"  - {warn}")

    if errors:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    analyze_project(path_to_check)
