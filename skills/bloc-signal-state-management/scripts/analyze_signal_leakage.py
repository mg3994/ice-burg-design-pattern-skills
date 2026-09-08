#!/usr/bin/env python3
"""
analyze_signal_leakage.py
Analyzes CubitSignal classes for proper resource disposal and equality overrides.
Checks:
- Signals and subscriptions created inside Cubits are disposed in close()
- CubitSignals implement custom equals parameter to prevent redundant re-renders
"""

import sys
import re
from pathlib import Path

def analyze_cubits(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    issues = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")

        if "extends CubitSignal" in content or "extends Cubit" in content:
            rel_path = dart_file.relative_to(lib_path)

            # Check 1: Custom equals function in super constructor
            if "CubitSignal" in content and "equals:" not in content:
                issues.append(f"{rel_path}: CubitSignal does not pass custom `equals` comparator to constructor. May cause redundant UI re-renders.")

            # Check 2: Signal instantiation vs disposal in close()
            signals_created = re.findall(r'final\s+(_?\w+)\s*=\s*signal\(', content)
            if signals_created:
                if "close()" not in content:
                    issues.append(f"{rel_path}: Defines signals ({', '.join(signals_created)}) but does not override close() for disposal.")
                else:
                    close_block = content[content.find("close()"): ]
                    for sig in signals_created:
                        if f"{sig}.dispose()" not in close_block:
                            issues.append(f"{rel_path}: Signal `{sig}` is not disposed in close(). Potential memory leak.")

    print(f"--- Signal & Cubit Leakage Analysis for: {lib_dir} ---")
    if not issues:
        print("✅ PASS: All CubitSignals pass equality checks and properly dispose signals.")
        sys.exit(0)

    print(f"⚠️ ISSUES DETECTED ({len(issues)}):")
    for issue in issues:
        print(f"  - {issue}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    analyze_cubits(path_to_check)
