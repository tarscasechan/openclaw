#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <handle> <message> [delay]" >&2
  exit 1
fi

target="$1"
shift
message="$1"
shift || true
delay="${1:-3m}"

name="direct-reminder-$(date +%Y%m%d-%H%M%S)"

openclaw cron add \
  --name "$name" \
  --description "[managed-by=direct-reminder] One-shot reminder to the contact's BlueBubbles account." \
  --at "$delay" \
  --delete-after-run \
  --session isolated \
  --channel bluebubbles \
  --to "$target" \
  --message "$message" \
  --announce \
  --expect-final \
  --timeout-seconds 60 \
  --json
