#!/usr/bin/env bash
# Who is actually contributing to the dojo?
#
# Siu's dojo has an analytics tab. Ours is git history, which is free, honest,
# and impossible to game without doing the work. Run it before a leadership call.
#
# Usage: scripts/adoption.sh [since]        e.g. scripts/adoption.sh "6 weeks ago"

# Deliberately NOT pipefail: every section here ends in `head`/`grep -q`, which
# close their pipe early and SIGPIPE the upstream `git log`. Under pipefail that
# reads as failure and the script reports "none" over real data.
set -eu
cd "$(dirname "$0")/.."

SINCE="${1:-3 months ago}"

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "Not a git repository yet, so there is nothing to measure."
  exit 1
fi

echo "Ling skills dojo, adoption since ${SINCE}"
echo

echo "== Skills in the library =="
# Directories only, at the exact depth, so the list and the count cannot disagree.
skills=$(find plugins -mindepth 3 -maxdepth 3 -type d -path '*/skills/*' | sort)
if [ -z "$skills" ]; then
  echo "  (empty)"
else
  echo "$skills" | while IFS= read -r s; do echo "  $(basename "$s")"; done
  echo "  ($(echo "$skills" | wc -l | tr -d ' ') total)"
fi
echo

echo "== Contributors =="
authors=$(git log --since="${SINCE}" --format='%aN' | sort | uniq -c | sort -rn)
if [ -z "$authors" ]; then
  echo "  no commits in this window"
else
  # Tab-separate first so names containing digits or spaces cannot be mis-split.
  echo "$authors" | sed -E 's/^ *([0-9]+) (.*)$/\2\t\1/' \
    | awk -F'\t' '{printf "  %-28s %s commits\n", $1, $2}'
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
