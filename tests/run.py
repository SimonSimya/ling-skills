#!/usr/bin/env python3
"""Regression suite for safety-check.py.

Every case here is one the scanner got wrong in review on 2026-08-18. A pattern
change that reopens any of them fails this suite. Run: python3 tests/run.py
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "safety-check.py"
SPEC = (ROOT / "tests" / "fixtures.md").read_text()


def cases(header):
    block = SPEC.split(f"## {header}")[1].split("##")[0]
    # Skip prose: only lines that are not blockquotes count as cases.
    return [l for l in block.splitlines()
            if l.strip() and not l.startswith("#") and not l.startswith(">")]


def run(line):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "skill"
        f.mkdir()
        (f / "SKILL.md").write_text(
            "# T\n## Definition of done\nPass condition: n/a.\nPrivilege level: read-only.\n")
        (f / "case.md").write_text(line + "\n")
        r = subprocess.run([sys.executable, str(CHECK), str(f)],
                           capture_output=True, text=True)
        return r.returncode, r.stdout


failures = []
for line in cases("MUST-LEAK"):
    code, out = run(line)
    if code != 2:
        failures.append(f"MISSED (exit {code}): {line.strip()[:70]}")

for line in cases("MUST-WARN"):
    code, out = run(line)
    if "  read " not in out:
        failures.append(f"NOT SURFACED: {line.strip()[:70]}")
    elif code == 2:
        failures.append(f"OVER-BLOCKED (should warn, not fail): {line.strip()[:70]}")

for line in cases("MUST-PASS"):
    code, out = run(line)
    if "hardcoded credential" in out:
        failures.append(f"FALSE POSITIVE on the recommended fix: {line.strip()[:70]}")

print(f"MUST-LEAK: {len(cases('MUST-LEAK'))} cases")
print(f"MUST-WARN: {len(cases('MUST-WARN'))} cases")
print(f"MUST-PASS: {len(cases('MUST-PASS'))} cases")
if failures:
    print("\n".join("  " + f for f in failures))
    print(f"\nFAIL: {len(failures)} regression(s)")
    sys.exit(1)
print("\nPASS: every case behaves as specified")
