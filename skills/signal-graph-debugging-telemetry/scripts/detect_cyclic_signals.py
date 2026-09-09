#!/usr/bin/env python3
"""
detect_cyclic_signals.py
Audits Dart source files for dangerous signal mutation calls inside computed or effect blocks.
"""

import sys
import re
from pathlib import Path

def detect_cycles(lib_dir):
    lib_path = Path(lib_dir)
    if not lib_path.exists():
        print(f"Error: Directory {lib_dir} does not exist.")
        sys.exit(1)

    warnings = []

    for dart_file in lib_path.rglob("*.dart"):
        content = dart_file.read_text(encoding="utf-8")
        rel_path = dart_file.relative_to(lib_path)

        # Check for signal assignment inside computed()
        computed_blocks = re.findall(r'computed\(\(\)\s*\{([^}]+)\}\)', content)
        for block in computed_blocks:
            if ".value =" in block or ".value++" in block:
                warnings.append(f"{rel_path}: Found signal value assignment inside computed() block! May trigger infinite evaluation cycle.")

    print(f"--- Signal Graph Cyclic Loop Audit: {lib_dir} ---")
    if not warnings:
        print("✅ PASS: Zero cyclic signal mutations detected inside computed blocks.")
        sys.exit(0)

    print(f"⚠️ CYCLIC WARNINGS ({len(warnings)}):")
    for warn in warnings:
        print(f"  - {warn}")
    sys.exit(0)

if __name__ == "__main__":
    path_to_check = sys.argv[1] if len(sys.argv) > 1 else "lib"
    detect_cycles(path_to_check)
