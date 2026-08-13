#!/usr/bin/env python3
"""Scan a skill folder before it enters the Ling dojo.

Usage: python3 scripts/safety-check.py <path-to-skill-folder> [...]

Exit 0 = clean. Exit 1 = blockers found. Warnings never fail the build.
The blockers are the three things that actually bite: secrets, machine-specific
paths, and references to files outside the skill folder (which break on install,
because plugins are copied to a cache).
"""

import re
import sys
from pathlib import Path

SECRETS = [
    (r"AIza[0-9A-Za-z_\-]{30,}", "Google API key"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI-style secret key"),
    (r"sk-ant-[A-Za-z0-9\-_]{20,}", "Anthropic API key"),
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub personal access token"),
    (r"xox[baprs]-[A-Za-z0-9\-]{10,}", "Slack token"),
    (r"ntn_[A-Za-z0-9]{20,}", "Notion token"),
    (r"Bearer\s+[A-Za-z0-9._\-]{20,}", "hardcoded bearer token"),
    (r"(?i)(api_key|apikey|secret|password|token)\s*[:=]\s*[\"'][^\"'{$\s]{8,}[\"']",
     "hardcoded credential"),
]

# Personal / machine-specific paths.
PATHS = [
    (r"/Users/[A-Za-z0-9._\-]+/", "absolute macOS home path"),
    (r"/home/[A-Za-z0-9._\-]+/", "absolute Linux home path"),
    (r"C:\\\\Users\\\\", "absolute Windows path"),
]

# Escapes the skill folder. Breaks once the plugin is cached.
ESCAPES = [(r"\.\./", "relative path escaping the skill folder")]

JUNK = {".DS_Store", "__pycache__", ".git", "node_modules", ".venv", "venv",
        ".pytest_cache", ".env"}

TEXT_SUFFIXES = {".md", ".py", ".js", ".ts", ".sh", ".json", ".yaml", ".yml", ".txt", ".toml"}


def scan(folder: Path):
    blockers, warnings = [], []

    if not folder.is_dir():
        return [(str(folder), 0, "path is not a directory")], []

    if not (folder / "SKILL.md").is_file():
        blockers.append((str(folder), 0, "no SKILL.md, this is not a skill"))

    for path in sorted(folder.rglob("*")):
        if any(part in JUNK for part in path.parts):
            warnings.append((path.name, 0, "development junk, remove before publishing"))
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            warnings.append((str(path), 0, f"unreadable: {exc}"))
            continue

        rel = path.relative_to(folder)
        for n, line in enumerate(lines, 1):
            for pattern, label in SECRETS:
                if re.search(pattern, line):
                    blockers.append((rel, n, f"{label}: never publish this, rotate it if it was real"))
            for pattern, label in PATHS:
                if re.search(pattern, line):
                    blockers.append((rel, n, f"{label}: only exists on your machine"))
            for pattern, label in ESCAPES:
                if re.search(pattern, line):
                    blockers.append((rel, n, f"{label}: breaks once the plugin is cached"))

    text = (folder / "SKILL.md").read_text(encoding="utf-8", errors="replace") \
        if (folder / "SKILL.md").is_file() else ""
    if "efinition of done" not in text:
        blockers.append(("SKILL.md", 0, "no 'Definition of done' section: no eval, no merge"))
    if not re.search(r"(?i)privilege level", text):
        warnings.append(("SKILL.md", 0, "no privilege level declared (read-only / draft-only / can-send)"))

    return blockers, warnings


def main():
    targets = [Path(a).expanduser().resolve() for a in sys.argv[1:]]
    if not targets:
        print(__doc__)
        return 2

    failed = False
    for folder in targets:
        blockers, warnings = scan(folder)
        print(f"\n=== {folder.name} ===")
        for where, line, msg in blockers:
            loc = f"{where}:{line}" if line else str(where)
            print(f"  BLOCK  {loc}: {msg}")
        for where, line, msg in warnings:
            loc = f"{where}:{line}" if line else str(where)
            print(f"  warn   {loc}: {msg}")
        if blockers:
            failed = True
        elif not warnings:
            print("  clean")
    print()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
