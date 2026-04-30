#!/usr/bin/env bash
set -euo pipefail

account="${GOG_ACCOUNT:-tarscasechan@gmail.com}"
keyring_password_file="$HOME/Library/Application Support/gogcli/keyring-password"
workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
state_dir="$workspace_dir/state/inbound-email"
state_file="$state_dir/replied.json"

if [[ -z "${GOG_KEYRING_PASSWORD:-}" ]]; then
  if [[ -r "$keyring_password_file" ]]; then
    export GOG_KEYRING_PASSWORD="$(cat "$keyring_password_file")"
  else
    echo "missing GOG_KEYRING_PASSWORD and $keyring_password_file" >&2
    exit 1
  fi
fi

mkdir -p "$state_dir"

contacts_json="$workspace_dir/state/contacts/cache.json"
if [[ ! -f "$contacts_json" ]]; then
  "$workspace_dir/scripts/contacts.sh" refresh >/dev/null
fi

python3 - "$contacts_json" "$state_file" <<'PY'
import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path

contacts_path = Path(sys.argv[1])
state_path = Path(sys.argv[2])
account = os.environ.get("GOG_ACCOUNT", "tarscasechan@gmail.com")
gog_keyring = os.environ.get("GOG_KEYRING_PASSWORD")
workspace = Path("/Users/tars/.openclaw/workspace")

def run(cmd):
    env = os.environ.copy()
    env["GOG_KEYRING_PASSWORD"] = gog_keyring
    return subprocess.check_output(cmd, text=True, env=env, cwd=str(workspace))

def load_state():
    if state_path.exists():
        try:
            return set(json.loads(state_path.read_text()).get("replied_message_ids", []))
        except Exception:
            return set()
    return set()

def save_state(ids):
    state_path.write_text(json.dumps({"replied_message_ids": sorted(ids)}, indent=2) + "\n")

def extract_text(payload):
    if not isinstance(payload, dict):
        return ""
    body = payload.get("body") or {}
    data = body.get("data")
    if data:
        try:
            return base64.urlsafe_b64decode(data + "==").decode("utf-8", "replace")
        except Exception:
            pass
    parts = payload.get("parts") or []
    texts = []
    for part in parts:
        if part.get("mimeType") == "text/plain":
            texts.append(extract_text(part))
        else:
            texts.append(extract_text(part))
    return "\n".join(t for t in texts if t)

def has_useful_body(message_id):
    raw = run(["gog", "-a", account, "gmail", "get", message_id, "--format=full", "-j", "--results-only"])
    msg = json.loads(raw)
    payload = ((msg or {}).get("message") or {}).get("payload") or {}
    text = extract_text(payload).strip()
    return bool(re.sub(r"\s+", "", text))

def requesty(subject):
    s = (subject or "").lower()
    return any(k in s for k in ["request", "please", "help", "generate", "idea", "ideas", "write", "how", "what", "can you", "need", "reply"])

contacts = json.loads(contacts_path.read_text()).get("contacts", [])
known_emails = set()
for c in contacts:
    for e in c.get("emails", []) or []:
        if e:
            known_emails.add(e.lower())

state = load_state()

search = run(["gog", "-a", account, "gmail", "search", "in:inbox is:unread newer_than:2d", "-j", "--results-only"])
messages = json.loads(search)

handled = []
for msg in messages:
    msg_id = msg.get("id")
    if not msg_id or msg_id in state:
        continue
    from_field = (msg.get("from") or "").lower()
    subject = msg.get("subject") or ""

    if not any(email in from_field for email in known_emails):
        continue
    if has_useful_body(msg_id):
        continue
    if not requesty(subject):
        continue

    m = re.search(r"<([^>]+)>", msg.get("from") or "")
    to_addr = m.group(1) if m else None
    if not to_addr:
        continue

    reply_body = (
        "Got it — I saw your email, but the body was empty. "
        "Please resend the request in the body so I can answer it properly."
    )
    run([
        "gog", "-a", account, "gmail", "send",
        "--to", to_addr,
        "--reply-to-message-id", msg_id,
        "--subject", f"Re: {subject}",
        "--body", reply_body,
        "-y",
    ])
    run(["gog", "-a", account, "gmail", "archive", msg_id, "-y"])
    handled.append(msg_id)

state.update(handled)
save_state(state)

print(json.dumps({"replied": handled, "count": len(handled)}, indent=2))
PY
