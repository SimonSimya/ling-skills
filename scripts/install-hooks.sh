#!/usr/bin/env bash
# Installs a pre-commit hook that runs the safety check before a commit lands.
# CI is the real enforcement. This is a convenience that catches a key BEFORE it
# enters your local history, where removing it means rewriting history rather than
# deleting a line. Note it scans your files as they are ON DISK, not what is
# staged, so a partial `git add` is not what it inspected.
#
#   ./scripts/install-hooks.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK="$ROOT/.git/hooks/pre-commit"

if [ -n "$(git -C "$ROOT" config --get core.hooksPath || true)" ]; then
  echo "core.hooksPath is set; this repo's .git/hooks is ignored. Install there instead." >&2
  exit 1
fi
if [ -e "$HOOK" ] && ! grep -q "install-hooks.sh" "$HOOK"; then
  echo "A pre-commit hook already exists and was not written by this script." >&2
  echo "Merge it by hand rather than losing it: $HOOK" >&2
  exit 1
fi

cat > "$HOOK" <<'INNER'
#!/usr/bin/env bash
# Auto-installed by scripts/install-hooks.sh
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"
status=0
while IFS= read -r skill; do
  python3 "$ROOT/scripts/safety-check.py" "$skill" || rc=$?
  rc=${rc:-0}
  [ "$rc" -eq 2 ] && status=2
  unset rc
done < <(find "$ROOT/plugins" -type d -name skills -exec find {} -mindepth 1 -maxdepth 1 -type d \; 2>/dev/null)

if [ "$status" -eq 2 ]; then
  echo ""
  echo "COMMIT BLOCKED: a secret, credential or internal id is in this tree."
  echo "Remove it and rotate the key if it was ever real."
  echo "Deliberate override (you had better be sure): git commit --no-verify"
  exit 1
fi
exit 0
INNER

chmod +x "$HOOK"
echo "pre-commit hook installed at .git/hooks/pre-commit"
