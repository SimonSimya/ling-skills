#!/usr/bin/env bash
# Who is actually contributing to the dojo?
#
# Siu's dojo has an analytics tab. Ours is git history, which is free, honest,
# and impossible to game without doing the work. Run it before a leadership call.
#
# Usage: scripts/adoption.sh [since]        e.g. scripts/adoption.sh "6 weeks ago"

set -euo pipefail
cd "$(dirname "$0")/.."

SINCE="${1:-3 months ago}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Not a git repository yet, so there is nothing to measure."
  exit 1
fi

echo "Ling skills dojo, adoption since ${SINCE}"
echo

echo "== Skills in the library =="
find plugins -type d -name skills -exec sh -c 'ls -1 "$1" 2>/dev/null' _ {} \; \
  | sort -u | sed 's/^/  /' || true
count=$(find plugins -mindepth 3 -maxdepth 3 -type d -path '*/skills/*' 2>/dev/null | wc -l | tr -d ' ')
echo "  (${count} total)"
echo

echo "== Contributors =="
if ! git log --since="${SINCE}" --format='%aN' 2>/dev/null | grep -q .; then
  echo "  no commits in this window"
else
  git log --since="${SINCE}" --format='%aN' | sort | uniq -c | sort -rn \
    | awk '{printf "  %-28s %s commits\n", substr($0, index($0,$2)), $1}'
fi
echo

echo "== Skills touched, most active first =="
git log --since="${SINCE}" --name-only --format= -- 'plugins/*/skills/*' 2>/dev/null \
  | grep -oE 'plugins/[^/]+/skills/[^/]+' | sort | uniq -c | sort -rn | head -20 \
  | sed 's/^/  /' || echo "  none"
echo

echo "== Not touched since ${SINCE} (prune candidates) =="
found=0
while IFS= read -r skill; do
  [ -z "$skill" ] && continue
  if [ -z "$(git log --since="${SINCE}" --format=%H -1 -- "$skill" 2>/dev/null)" ]; then
    last=$(git log --format=%as -1 -- "$skill" 2>/dev/null || echo "never committed")
    echo "  $(basename "$skill")  (last touched: ${last:-never})"
    found=1
  fi
done < <(find plugins -mindepth 3 -maxdepth 3 -type d -path '*/skills/*' 2>/dev/null)
[ "$found" -eq 0 ] && echo "  none, everything has been touched"
echo
echo "Kill criteria: who asked for it, does it connect to value within two steps,"
echo "and has anyone acted on its output in three weeks? If no, retire it."
