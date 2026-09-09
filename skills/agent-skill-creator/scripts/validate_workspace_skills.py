#!/usr/bin/env python3
"""
validate_workspace_skills.py
Validates all agent skills in the workspace using skills_ref.cli.
"""

import sys
import subprocess
from pathlib import Path

def validate_all_skills(skills_dir="skills"):
    skills_path = Path(skills_dir)
    if not skills_path.exists():
        print(f"Directory {skills_dir} does not exist.")
        sys.exit(1)

    failed = False
    skill_dirs = [d for d in skills_path.iterdir() if d.is_dir()]

    print(f"--- Validating {len(skill_dirs)} Agent Skills in `{skills_dir}/` ---")
    for skill in sorted(skill_dirs):
        cmd = [sys.executable, "-m", "skills_ref.cli", "validate", str(skill)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ {skill.name}: VALID")
        else:
            print(f"  ❌ {skill.name}: INVALID")
            print(f"     {result.stdout.strip() or result.stderr.strip()}")
            failed = True

    if failed:
        print("\n❌ One or more skills failed validation.")
        sys.exit(1)

    print("\n✅ ALL SKILLS PASSED VALIDATION!")
    sys.exit(0)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "skills"
    validate_all_skills(path)
