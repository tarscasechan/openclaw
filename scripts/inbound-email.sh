#!/usr/bin/env bash
set -euo pipefail

account="${GOG_ACCOUNT:-tarscasechan@gmail.com}"
keyring_password_file="$HOME/Library/Application Support/gogcli/keyring-password"
dry_run=false

usage() {
  cat <<'EOF'
usage:
  scripts/inbound-email.sh [--dry-run]

Behavior:
  - refreshes local Contacts cache
  - keeps Gmail Inbox mail from known contact emails
  - archives everything else in Inbox
EOF
}

for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $arg" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "${GOG_KEYRING_PASSWORD:-}" ]]; then
  if [[ -r "$keyring_password_file" ]]; then
    export GOG_KEYRING_PASSWORD="$(cat "$keyring_password_file")"
  else
    echo "missing GOG_KEYRING_PASSWORD and $keyring_password_file" >&2
    exit 1
  fi
fi

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cache_file="$workspace_dir/state/contacts/cache.json"

"$workspace_dir/scripts/contacts.sh" refresh >/dev/null

if ! query="$(python3 - "$cache_file" <<'PY'
import json
import re
import sys

cache_path = sys.argv[1]
with open(cache_path, 'r', encoding='utf-8') as f:
    cache = json.load(f)

emails = []
seen = set()
for contact in cache.get('contacts', []):
    for email in contact.get('emails', []) or []:
        email = email.strip()
        if not email:
            continue
        key = email.lower()
        if key not in seen:
            seen.add(key)
            emails.append(email)

if not emails:
    print('no contact emails found in Contacts cache', file=sys.stderr)
    raise SystemExit(1)

parts = ' OR '.join(emails)
print(f'in:inbox -from:({parts})')
PY
)"; then
  exit 1
fi

if $dry_run; then
  echo "query: $query"
  exit 0
fi

gog -a "$account" gmail archive --query "$query" --max 100 -j --results-only >/dev/null

"$workspace_dir/scripts/inbound-email-reply.sh" >/dev/null

echo "processed inbox with query: $query"
