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
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub classic token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "GitHub fine-grained token"),
    (r"gh[opsu]_[A-Za-z0-9]{20,}", "GitHub OAuth/app token"),
    (r"glpat-[A-Za-z0-9_\-]{10,}", "GitLab personal access token"),
    (r"xox[baprs]-[A-Za-z0-9\-]{10,}", "Slack token"),
    (r"ntn_[A-Za-z0-9]{20,}", "Notion token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key id"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key material"),
    (r"Bearer\s+[A-Za-z0-9._\-]{20,}", "hardcoded bearer token"),
    # Quoted or bare. Bare form is how .env and YAML actually leak.
    (r"(?i)\b(api[_-]?key|secret|password|passwd|token|client[_-]?secret)\b\s*[:=]\s*"
     r"[\"']?[^\s\"'{$<>][^\s\"']{7,}", "hardcoded credential"),
]

# Personal / machine-specific paths.
PATHS = [
    (r"/Users/[A-Za-z0-9._\-]+/", "absolute macOS home path"),
    (r"/home/[A-Za-z0-9._\-]+/", "absolute Linux home path"),
    (r"C:\\\\Users\\\\", "absolute Windows path"),
    (r"(?<![\w.])~/", "home-relative path (only resolves on your machine)"),
]

# Escapes the skill folder. Breaks once the plugin is cached.
ESCAPES = [(r"\.\./", "relative path escaping the skill folder")]

JUNK = {".DS_Store", "__pycache__", ".git", "node_modules", ".venv", "venv",
        ".pytest_cache"}

# Files that must never ship, whatever their contents.
FORBIDDEN_NAMES = {".env", ".netrc", "id_rsa", "id_ed25519", "credentials"}
FORBIDDEN_SUFFIXES = {".pem", ".p12", ".pfx", ".key", ".keystore"}

# Scan everything except known-binary formats. An allowlist silently skips
# whatever file type nobody thought of, which is where secrets hide.
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
                   ".gz", ".tgz", ".bz2", ".xz", ".woff", ".woff2", ".ttf", ".otf",
                   ".mp3", ".mp4", ".mov", ".wav", ".so", ".dylib", ".bin", ".sqlite"}


def scan(folder: Path):
    blockers, warnings = [], []

    if not folder.is_dir():
        return [(str(folder), 0, "path is not a directory")], []

    if not (folder / "SKILL.md").is_file():
        blockers.append((str(folder), 0, "no SKILL.md, this is not a skill"))

    try:
        entries = sorted(folder.rglob("*"))
    except OSError as exc:
        return [(str(folder), 0, f"could not traverse: {exc}")], []

    for path in entries:
        if any(part in JUNK for part in path.parts):
            warnings.append((path.name, 0, "development junk, remove before publishing"))
            continue
        if not path.is_file():
            continue

        rel = path.relative_to(folder)
        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            blockers.append((rel, 0, "credential file, must never be published"))
            continue
        if path.is_symlink():
            warnings.append((rel, 0, "symlink, verify the target ships with the skill"))
        if path.suffix.lower() in BINARY_SUFFIXES:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            warnings.append((str(rel), 0, f"unreadable: {exc}"))
            continue

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

    skill_md = folder / "SKILL.md"
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        if "efinition of done" not in text:
            blockers.append(("SKILL.md", 0, "no 'Definition of done' section: no eval, no merge"))
        if not re.search(r"(?i)privilege level", text):
            warnings.append(("SKILL.md", 0,
                             "no privilege level declared (read-only / draft-only / can-send)"))

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
