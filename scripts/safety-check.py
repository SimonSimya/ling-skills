#!/usr/bin/env python3
"""Scan a skill folder before it enters the Ling dojo.

Usage: python3 scripts/safety-check.py <path-to-skill-folder> [...]

Exit 0 = clean. Exit 1 = blockers found. Warnings never fail the build.
Four categories, matching the AH course's safety review: secrets, personal/
machine-specific paths, references escaping the skill folder (breaks on
install, plugins are copied to a cache), and dangerous or too-machine-specific
scripts (destructive commands, credential-store reads, exfiltration).
"""

import re
import sys
from pathlib import Path

# Dangerous or too-machine-specific behavior, the 4th category in the lesson's
# safety review (secrets / personal data / broken refs / dangerous scripts).
# Ported from .claude/skills/export-skill/SKILL.md's block-export checklist.
DANGEROUS = [
    (r"\bcurl\b[^\n|]*\|\s*(sudo\s+)?(ba)?sh\b", "curl piped into a shell"),
    (r"\bwget\b[^\n|]*\|\s*(sudo\s+)?(ba)?sh\b", "wget piped into a shell"),
    (r"\beval\s*\(\s*(base64|atob|Buffer\.from)", "eval of decoded/obfuscated content"),
    (r"\bexec\s*\(\s*(base64|atob|requests\.get|urlopen|fetch)", "exec of downloaded/obfuscated content"),
    (r"\brm\s+-rf\s+(/(?!tmp|private/tmp)\S*|~(?!/(Downloads|Desktop|tmp))\S*|\$HOME\b)",
     "rm -rf against a broad or home-relative path"),
    (r"\bchmod\s+(-R\s+)?777\b", "chmod 777"),
    (r"(?<![\w/])(/etc|/usr|/bin|/sbin|/System)/\S", "write target under a system directory"),
    (r"\bcrontab\b\s+-", "crontab edit"),
    (r"~/\.ssh\b|~/\.aws\b|Login Data|Cookies\.sqlite|keychain\b(?!.*#)",
     "reads SSH keys, cloud creds, browser credential stores, or the keychain"),
    (r"(?i)\bpost(ing)?\b[^\n]{0,40}\b(env|environ|\.env|credentials?|secrets?)\b[^\n]{0,40}"
     r"\b(http|https|fetch|requests?\.(post|put))\b",
     "posts env vars or credentials to a network endpoint"),
]

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

# Portable by construction: these LOOK machine-specific to PATHS/DANGEROUS but
# resolve identically on every machine that runs Claude Code, so matching them is
# always a false positive. Kept as one list because they are one shape, not two
# incidents: a standard interpreter declaration, and the tool's own config tree.
# Without this, safety-check BLOCKs any skill shipping a Python script (the
# `#!/usr/bin/env python3` shebang hits the /usr rule) or documenting where
# transcripts live. Found 2026-08-17 running this against the objection-gate-pack:
# 4 BLOCKs, 4 false positives, 0 real findings. The dojo's own plugin is
# SKILL.md-only, which is why the 13 Aug test came back clean.
PORTABLE = [
    r"^#!/(usr/bin|bin)/",            # shebang, only ever line 1
    r"(?<![\w.])~/\.claude(/|\b)",    # Claude Code's config tree
    r"(?<![\w.])~/\.config(/|\b)",    # XDG config, same reasoning
]

# PORTABLE suppresses "this path is machine-specific". It must NEVER suppress
# "this path is being written to", and these run on the RAW line for that reason.
# ~/.claude is the highest-value write target on a reviewer's machine: appending
# to settings.local.json grants permissions, and a file dropped in agents/ or
# hooks/ executes. A skill has no business writing there; it ships skills, not
# config. Added 2026-08-17 after the PORTABLE fix above opened exactly this hole
# and the fix's own test never exercised it (caught by the round-2 objection
# gate with a planted file, not by me).
CONFIG_HOME = r"(~|\$HOME|\bPath\.home\(\))\s*[/,]?\s*['\"]?\.(claude|config)\b"
CONFIG_WRITES = [
    (rf">>?\s*['\"]?[^\s'\"]*{CONFIG_HOME}", "shell redirect into the Claude/XDG config tree"),
    (rf"\b(cp|mv|tee|install|rsync|ln)\b[^\n]*{CONFIG_HOME}",
     "copies, moves or links a file into the Claude/XDG config tree"),
    (rf"\brm\b[^\n]*{CONFIG_HOME}", "deletes inside the Claude/XDG config tree"),
    (rf"\bopen\s*\([^)]*{CONFIG_HOME}[^)]*['\"][waxr]?\+?[wax]",
     "opens a file in the Claude/XDG config tree for writing"),
    (rf"\b(write_text|write_bytes|mkdir|touch|unlink|chmod)\b[^\n]*{CONFIG_HOME}",
     "writes into the Claude/XDG config tree"),
    (rf"{CONFIG_HOME}[^\n]*\b(write_text|write_bytes|unlink|mkdir)\b",
     "writes into the Claude/XDG config tree"),
]

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
            # Blank out the portable references, then run the machine-specificity
            # rules on what is left. Blanking rather than skipping the whole line
            # keeps a real finding that shares a line with a portable one.
            scrubbed = line
            for pattern in PORTABLE:
                scrubbed = re.sub(pattern, "", scrubbed)

            for pattern, label in SECRETS:
                if re.search(pattern, line):
                    blockers.append((rel, n, f"{label}: never publish this, rotate it if it was real"))
            for pattern, label in PATHS:
                if re.search(pattern, scrubbed):
                    blockers.append((rel, n, f"{label}: only exists on your machine"))
            for pattern, label in ESCAPES:
                if re.search(pattern, line):
                    blockers.append((rel, n, f"{label}: breaks once the plugin is cached"))
            for pattern, label in DANGEROUS:
                if re.search(pattern, scrubbed):
                    blockers.append((rel, n, f"{label}: dangerous or too machine-specific to publish"))
            # Raw line, not scrubbed: PORTABLE must not be able to hide a write.
            for pattern, label in CONFIG_WRITES:
                if re.search(pattern, line):
                    blockers.append((rel, n, f"{label}: a skill ships skills, not config"))

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
