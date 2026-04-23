#!/usr/bin/env bash
set -euo pipefail

want_name="git checkpoint"
want_tag="[managed-by=workspace.autocommit]"
want_desc="$want_tag Review workspace changes, commit in logical groups, push."
want_cron="15 */6 * * *"
want_tz="America/Los_Angeles"

want_message="$(cat <<EOF
You are maintaining the git repo at ~/.openclaw/workspace.

Goal: keep the repo up to date with high-signal commits.

Process:
- cd ~/.openclaw/workspace
- If not a git repo, exit with an error.
- If on a non-main branch, do nothing (NO_REPLY).
- If merge/rebase in progress, do nothing (NO_REPLY).
- If there are no changes (git status clean), reply with NO_REPLY.
- Otherwise, identify logical groups of changes and create one commit per group.
- Follow the repo commit format: directive title + body with Prompt: ... then Context: bullets.
- Avoid committing secrets, machine state, caches, or anything ignored by git.
- Use git status/diff/log to understand changes before committing.
- Stage only what belongs to each commit (git add <paths>), then commit.
- After all commits, push to origin/main.

Final reply:
- If commits were created: list the new commit hashes and titles.
- If nothing to do: NO_REPLY.
EOF
)"

jobs_json="$(openclaw cron list --json)"

job_id="$(
  JOBS_JSON="$jobs_json" WANT_NAME="$want_name" WANT_TAG="$want_tag" node <<JS
const input = process.env.JOBS_JSON;
const wantName = process.env.WANT_NAME;
const wantTag = process.env.WANT_TAG;
const j = JSON.parse(input);
const matches = (j.jobs || []).filter(job =>
  job.name === wantName ||
  (typeof job.description === "string" && job.description.includes(wantTag))
);
if (matches.length === 0) process.exit(0);
if (matches.length > 1) {
  console.error("Multiple matching cron jobs found:", matches.map(m => m.id).join(", "));
  process.exit(2);
}
process.stdout.write(matches[0].id);
JS
)"

if [[ -n "${job_id:-}" ]]; then
  openclaw cron edit "$job_id" \
    --name "$want_name" \
    --description "$want_desc" \
    --cron "$want_cron" \
    --tz "$want_tz" \
    --session isolated \
    --message "$want_message" \
    --tools exec \
    --light-context \
    --no-deliver >/dev/null
  echo "Updated cron job: $want_name ($job_id)"
  exit 0
fi

created="$(
  openclaw cron add \
    --name "$want_name" \
    --description "$want_desc" \
    --cron "$want_cron" \
    --tz "$want_tz" \
    --session isolated \
    --message "$want_message" \
    --tools exec \
    --light-context \
    --no-deliver \
    --json
)"

new_id="$(
  CREATED="$created" node <<JS
const j = JSON.parse(process.env.CREATED);
process.stdout.write(j.id);
JS
)"
echo "Created cron job: $want_name ($new_id)"

