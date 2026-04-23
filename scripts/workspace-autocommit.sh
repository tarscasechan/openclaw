#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root_dir"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repository: $root_dir" >&2
  exit 2
fi

branch="$(git branch --show-current || true)"
if [[ "$branch" != "main" ]]; then
  echo "Refusing to commit on non-main branch: $branch" >&2
  exit 3
fi

if [[ -d .git/rebase-apply || -d .git/rebase-merge || -f .git/MERGE_HEAD ]]; then
  echo "Refusing to run during merge/rebase." >&2
  exit 4
fi

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
fi

if [[ -z "$(git status --porcelain)" ]]; then
  exit 0
fi

now_utc="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

git commit -m "$(cat <<EOF
Checkpoint workspace

Prompt: Save a periodic checkpoint of durable workspace changes as of $now_utc.

Context:
- Automated checkpoint to keep repo up to date
- Skips when there are no working tree changes
EOF
)"

git push
