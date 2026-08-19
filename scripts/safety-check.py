#!/usr/bin/env python3
"""Scan a skill folder before it enters the Ling dojo.

Usage: python3 scripts/safety-check.py <skill-folder-or-submission.zip> [...]

Exit 0 = clean. Exit 1 = blockers found. Warnings never fail the build.
Four categories, matching the AH course's safety review: secrets, personal/
machine-specific paths, references escaping the skill folder (breaks on
install, plugins are copied to a cache), and dangerous or too-machine-specific
scripts (destructive commands, credential-store reads, exfiltration).
"""

import re
import shutil
import sys
import tempfile
import zipfile
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

# ---------------------------------------------------------------------------
# Contributed-submission categories. Added 2026-08-18, when the first four real
# submissions arrived in Slack from people who are not engineers. The original
# four categories answer "will this break or bite the installer". These answer
# "does this leak Ling", which is a different question and the one Simon asked.
# ---------------------------------------------------------------------------

# Vendor credentials the original SECRETS list did not cover. Every one of these
# is live-money or live-data on a Ling account.
VENDOR_SECRETS = [
    (r"\b(sk|rk)_live_[A-Za-z0-9]{10,}", "Stripe LIVE secret key"),
    (r"\bwhsec_[A-Za-z0-9]{10,}", "Stripe webhook signing secret"),
    (r"\bpk_live_[A-Za-z0-9]{10,}", "Stripe live publishable key"),
    (r'"type"\s*:\s*"service_account"', "GCP/Firebase service-account JSON"),
    (r"\bSG\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}", "SendGrid API key"),
    (r"\bSK[0-9a-fA-F]{32}\b", "Twilio API key"),
    (r"\bAC[0-9a-fA-F]{32}\b", "Twilio account SID"),
    (r"\bkey-[0-9a-zA-Z]{32}\b", "Mailgun API key"),
    (r"\bpat-(na|eu)\d-[0-9a-fA-F\-]{20,}", "HubSpot private-app token"),
    (r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", "JWT"),
    (r"(?i)\bamplitude[^\n]{0,30}\b(api[_-]?key|secret)\b[^\n]{0,10}[:=]\s*\S{8,}",
     "Amplitude API credential"),
    (r"(?i)\bmongodb(\+srv)?://[^\s:@]+:[^\s@]+@", "MongoDB connection string with password"),
    (r"(?i)\b(postgres(ql)?|mysql|redis)://[^\s:@]+:[^\s@]+@",
     "database connection string with password"),
]

# Internal identifiers. Not secret in the cryptographic sense, but they name
# Ling's actual accounts, dashboards and documents, and a public repo hands an
# outsider the map. These are blockers because the skill should read them from
# config or ask the user, which the portability checklist already requires.
INTERNAL_IDS = [
    (r"\bacct_[A-Za-z0-9]{10,}", "Stripe account id"),
    (r"\bcus_[A-Za-z0-9]{10,}", "Stripe customer id"),
    (r"\b(sub|in|pi|ch)_[A-Za-z0-9]{14,}", "Stripe object id"),
    (r"https?://docs\.google\.com/[a-z]+/d/[A-Za-z0-9_\-]{25,}", "Google Doc/Sheet URL with file id"),
    (r"https?://drive\.google\.com/drive/folders/[A-Za-z0-9_\-]{25,}", "Google Drive folder id"),
    (r"(?i)\b(spreadsheet|sheet|folder|document|file)[_-]?id\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{25,}",
     "hardcoded Google file id"),
    (r"\bhttps?://[a-z0-9-]+\.slack\.com/archives/[CGD][A-Z0-9]{8,}", "Slack channel permalink"),
    (r"(?i)\bchannel[_-]?id\b\s*[:=]\s*['\"]?[CGD][A-Z0-9]{8,}", "hardcoded Slack channel id"),
    (r"(?i)\b(list|space|folder|team)[_-]?id\b\s*[:=]\s*['\"]?\d{7,}", "hardcoded ClickUp id"),
    (r"(?i)\bproperties/\d{9,}", "GA4 property id"),
    (r"(?i)\bprojectId\b\s*[:=]\s*['\"][a-z0-9-]{6,}['\"]", "hardcoded Firebase/GCP project id"),
]

# Customer and colleague data. A skill is a process; it should never carry the
# rows it was tested on. Warnings, not blockers, because a role address in an
# owner field is legitimate and only a human can tell the difference.
PII = [
    (r"[A-Za-z0-9._%%+\-]+@(?!ling-app\.com|simyasolutions\.com|example\.(com|org))"
     r"[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", "external email address, possibly a real user"),
    (r"(?<!\d)\+?\d{1,3}[\s.\-]?\(?\d{2,4}\)?[\s.\-]?\d{3,4}[\s.\-]?\d{3,4}(?!\d)",
     "possible phone number"),
    (r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b", "possible payment card number"),
]

# Business-confidential content. No regex decides this; it flags passages a human
# must read before the repo goes public. Ling's revenue, roadmap and salary data
# are the things that actually hurt, and none of them look like a credential.
BUSINESS = [
    (r"(?i)\b(ARR|MRR|revenue|churn rate|LTV|CAC|runway|burn rate)\b[^\n]{0,40}"
     r"[\$€£]\s?[\d,.]+|[\$€£]\s?[\d,.]+[^\n]{0,20}\b(ARR|MRR|revenue)\b",
     "revenue or growth figure"),
    (r"(?i)\b(salary|salaries|compensation|payroll|equity grant|option grant)\b",
     "compensation reference"),
    (r"(?i)\b(acquisition|term sheet|due diligence|cap table|valuation|fundrais\w+)\b",
     "corporate-finance reference"),
    (r"(?i)\b(confidential|internal only|do not share|nda)\b", "explicitly marked confidential"),
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
            for pattern, label in VENDOR_SECRETS:
                if re.search(pattern, line):
                    blockers.append((rel, n, f"{label}: never publish this, ROTATE IT NOW"))
            for pattern, label in INTERNAL_IDS:
                if re.search(pattern, line):
                    blockers.append((rel, n, f"{label}: read it from config or ask the user"))
            for pattern, label in PII:
                if re.search(pattern, line):
                    warnings.append((rel, n, f"{label}: a skill is a process, not the rows it was tested on"))
            for pattern, label in BUSINESS:
                if re.search(pattern, line):
                    warnings.append((rel, n, f"{label}: a human must read this before the repo is public"))

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
    for target in targets:
        # Submissions arrive as zips from Slack, so accept one directly rather
        # than making the reviewer unpack it by hand. An unpack step a human has
        # to remember is a step that gets skipped on a busy day.
        tmp = None
        folder = target
        if target.is_file() and target.suffix.lower() == ".zip":
            tmp = Path(tempfile.mkdtemp(prefix="safety-check-"))
            try:
                with zipfile.ZipFile(target) as z:
                    for member in z.namelist():
                        # Refuse path traversal rather than trusting the archive.
                        dest = (tmp / member).resolve()
                        if not str(dest).startswith(str(tmp.resolve())):
                            print(f"\n=== {target.name} ===")
                            print(f"  BLOCK  {member}: zip entry escapes the archive root")
                            failed = True
                            z = None
                            break
                    if z is not None:
                        z.extractall(tmp)
            except zipfile.BadZipFile as exc:
                print(f"\n=== {target.name} ===")
                print(f"  BLOCK  {target.name}: not a readable zip: {exc}")
                shutil.rmtree(tmp, ignore_errors=True)
                failed = True
                continue
            # A zip usually wraps everything in one top-level directory.
            kids = [c for c in tmp.iterdir() if c.name != "__MACOSX"]
            folder = kids[0] if len(kids) == 1 and kids[0].is_dir() else tmp

        blockers, warnings = scan(folder)
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
        print(f"\n=== {target.name} ===")
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
