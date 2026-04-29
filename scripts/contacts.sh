#!/usr/bin/env bash
set -euo pipefail

die() {
  echo "contacts: $*" >&2
  exit 1
}

usage() {
  cat <<'EOF'
usage:
  scripts/contacts.sh refresh
  scripts/contacts.sh resolve <query>

env:
  OPENCLAW_CONTACTS_CACHE_DIR  override cache directory (default: ./state/contacts)
EOF
}

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cache_dir="${OPENCLAW_CONTACTS_CACHE_DIR:-$workspace_dir/state/contacts}"
cache_file="$cache_dir/cache.json"

refresh_cache() {
  mkdir -p "$cache_dir"
  chmod 700 "$cache_dir" 2>/dev/null || true

  local raw_tsv
  raw_tsv="$(osascript <<'APPLESCRIPT'
on replace_text(theText, searchString, replacementString)
  set AppleScript's text item delimiters to searchString
  set theItems to text items of theText
  set AppleScript's text item delimiters to replacementString
  set theText to theItems as text
  set AppleScript's text item delimiters to ""
  return theText
end replace_text

on sanitize(theText)
  set cleaned to theText as text
  set cleaned to my replace_text(cleaned, tab, " ")
  set cleaned to my replace_text(cleaned, return, " ")
  set cleaned to my replace_text(cleaned, linefeed, " ")
  return cleaned
end sanitize

on join_list(values, delim)
  if values is {} then return ""
  set AppleScript's text item delimiters to delim
  set out to values as text
  set AppleScript's text item delimiters to ""
  return out
end join_list

tell application "Contacts"
  set rows to {}
  repeat with p in people
    set contactName to my sanitize(name of p)

    set emailValues to {}
    try
      repeat with e in emails of p
        set end of emailValues to my sanitize(value of e)
      end repeat
    end try

    set phoneValues to {}
    try
      repeat with ph in phones of p
        set end of phoneValues to my sanitize(value of ph)
      end repeat
    end try

    set end of rows to contactName & tab & my join_list(emailValues, "|") & tab & my join_list(phoneValues, "|")
  end repeat

  return rows as text
end tell
APPLESCRIPT
)" || die "could not read Contacts.app; grant access when macOS prompts for Contacts"

  printf '%s\n' "$raw_tsv" | python3 - "$cache_file" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone

out_path = sys.argv[1]
tmp_path = out_path + ".tmp"

contacts = []
for line in sys.stdin.read().splitlines():
    if not line.strip():
        continue
    parts = line.split("\t")
    while len(parts) < 3:
        parts.append("")
    name, emails, phones = (part.strip() for part in parts[:3])
    contacts.append(
        {
            "name": name,
            "emails": [item for item in emails.split("|") if item],
            "phones": [item for item in phones.split("|") if item],
        }
    )

payload = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source": "macos-contacts",
    "contacts": contacts,
}

with open(tmp_path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2, ensure_ascii=False)
    handle.write("\n")

os.replace(tmp_path, out_path)
os.chmod(out_path, 0o600)
PY

  echo "$cache_file"
}

resolve_contact() {
  local query="${1:-}"
  [[ -n "$query" ]] || die "resolve needs a query"

  if [[ ! -f "$cache_file" ]]; then
    refresh_cache >/dev/null
  fi

  python3 - "$cache_file" "$query" <<'PY'
import json
import re
import sys

cache_path, query = sys.argv[1], sys.argv[2].strip()
q_lower = query.lower()

def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9@+]+", "", text.lower())

def score_contact(contact):
    name = contact.get("name", "")
    emails = contact.get("emails", []) or []
    phones = contact.get("phones", []) or []

    fields = [name, *emails, *phones]
    best = 0
    for field in fields:
        f_lower = field.lower()
        f_norm = norm(field)
        if q_lower == f_lower:
            best = max(best, 100)
        if f_lower == q_lower and "@" in q_lower:
            best = max(best, 100)
        if f_norm and f_norm == norm(query):
            best = max(best, 98)
        if q_lower in f_lower:
            best = max(best, 80)
        if norm(query) and norm(query) in f_norm:
            best = max(best, 70)
    return best

with open(cache_path, "r", encoding="utf-8") as handle:
    cache = json.load(handle)

matches = []
for contact in cache.get("contacts", []):
    score = score_contact(contact)
    if score:
        matches.append((score, contact))

if not matches:
    print(f"no match for: {query}", file=sys.stderr)
    raise SystemExit(1)

matches.sort(key=lambda item: (-item[0], item[1].get("name", "").lower()))
score, contact = matches[0]
emails = ", ".join(contact.get("emails", [])) or "(none)"
phones = ", ".join(contact.get("phones", [])) or "(none)"

print(contact.get("name", "(unnamed)"))
print(f"emails: {emails}")
print(f"phones: {phones}")
if len(matches) > 1:
    print(f"matches: {len(matches)} total; best score {score}")
PY
}

main() {
  case "${1:-}" in
    refresh)
      refresh_cache
      ;;
    resolve)
      shift
      resolve_contact "${1:-}"
      ;;
    ""|-h|--help|help)
      usage
      ;;
    *)
      usage >&2
      exit 1
      ;;
  esac
}

main "$@"
