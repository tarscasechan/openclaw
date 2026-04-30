#!/usr/bin/env python3
"""Historical backfill for proof-gate.

Scans assistant final answers from sessions before the proof-gate baseline,
finds unsupported claim patterns, and writes a discovery report plus candidate
cases. This intentionally does not change the live proof-gate state: historical
failures are mining input, not current regressions.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
PROOF_GATE_PATH = ROOT / "scripts" / "proof-gate-eval.py"
LOG_DIR = ROOT / "logs" / "proof-gate"
STATE_DIR = ROOT / "state" / "proof-gate"
BASELINE_FILE = STATE_DIR / "baseline.json"
BACKFILL_LATEST = LOG_DIR / "backfill-latest.json"
BACKFILL_HISTORY = LOG_DIR / "backfill-history.jsonl"
CANDIDATES_FILE = ROOT / "evals" / "proof-gate-backfill-candidates.json"

spec = importlib.util.spec_from_file_location("proof_gate_eval", PROOF_GATE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit(f"cannot import {PROOF_GATE_PATH}")
proof_gate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = proof_gate
spec.loader.exec_module(proof_gate)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return default


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def compact_text(text: str, max_chars: int = 700) -> str:
    compact = " ".join((text or "").split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 1] + "…"


def stable_id(text: str) -> str:
    return hashlib.sha1(" ".join(text.split()).encode("utf-8")).hexdigest()[:12]


def iter_session_files() -> Iterable[Path]:
    sdir = proof_gate.session_dir()
    if not sdir.exists():
        return []
    files = []
    for path in sdir.glob("*.jsonl"):
        name = path.name
        if ".checkpoint." in name or ".trajectory" in name or ".deleted." in name:
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.stat().st_mtime)


def iter_final_messages(before: datetime | None, after: datetime | None, limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in iter_session_files():
        try:
            with path.open() as f:
                for line_no, line in enumerate(f, start=1):
                    try:
                        event = json.loads(line)
                    except Exception:
                        continue
                    if event.get("type") != "message":
                        continue
                    message = event.get("message") or {}
                    if message.get("role") != "assistant":
                        continue
                    ts = proof_gate.parse_ts(event.get("timestamp"))
                    if not ts:
                        continue
                    if before and ts >= before:
                        continue
                    if after and ts < after:
                        continue
                    for item in message.get("content") or []:
                        if item.get("type") != "text" or not proof_gate.is_final_text(item):
                            continue
                        text = item.get("text") or ""
                        if text in {"NO_REPLY", "HEARTBEAT_OK"}:
                            continue
                        rows.append(
                            {
                                "timestamp": ts.isoformat().replace("+00:00", "Z"),
                                "session_file": str(path),
                                "line": line_no,
                                "text": text,
                                "fingerprint": stable_id(text),
                            }
                        )
                        if len(rows) >= limit:
                            return rows
        except OSError:
            continue
    rows.sort(key=lambda r: r["timestamp"])
    return rows


def build_candidates(flagged: list[dict[str, Any]], per_code: int) -> list[dict[str, Any]]:
    by_code: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for row in flagged:
        for violation in row["violations"]:
            key = (violation["code"], row["fingerprint"])
            if key in seen:
                continue
            seen.add(key)
            if len(by_code[violation["code"]]) >= per_code:
                continue
            by_code[violation["code"]].append(
                {
                    "id": f"backfill_{violation['code']}_{row['fingerprint']}",
                    "text": compact_text(row["text"]),
                    "expect_ok": False,
                    "expect_codes": [violation["code"]],
                    "source": {
                        "timestamp": row["timestamp"],
                        "session_file": row["session_file"],
                        "line": row["line"],
                    },
                    "reason": violation,
                }
            )
    candidates: list[dict[str, Any]] = []
    for code in sorted(by_code):
        candidates.extend(by_code[code])
    return candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="Mine historical proof-gate failures from pre-baseline sessions.")
    parser.add_argument("--limit", type=int, default=5000, help="Max final answers to scan.")
    parser.add_argument("--after", default="", help="Optional ISO timestamp lower bound.")
    parser.add_argument("--before", default="", help="Optional ISO timestamp upper bound. Defaults to proof-gate baseline.")
    parser.add_argument("--candidates-per-code", type=int, default=5, help="Candidate examples to save per violation code.")
    parser.add_argument("--json", action="store_true", help="Print full JSON report.")
    parser.add_argument("--fail-on-flags", action="store_true", help="Exit nonzero if historical flags are found.")
    args = parser.parse_args()

    baseline = load_json(BASELINE_FILE, {})
    before = proof_gate.parse_ts(args.before) if args.before else proof_gate.parse_ts(baseline.get("created_at"))
    after = proof_gate.parse_ts(args.after) if args.after else None

    messages = iter_final_messages(before=before, after=after, limit=args.limit)
    flagged: list[dict[str, Any]] = []
    by_code: Counter[str] = Counter()
    by_session: Counter[str] = Counter()
    for row in messages:
        violations = proof_gate.find_violations(row["text"])
        if not violations:
            continue
        item = {**row, "text_excerpt": compact_text(row["text"]), "violations": [v.to_json() for v in violations]}
        flagged.append(item)
        by_session[row["session_file"]] += 1
        for violation in violations:
            by_code[violation.code] += 1

    candidates = build_candidates(flagged, args.candidates_per_code)
    write_json(CANDIDATES_FILE, candidates)

    report_examples = [{k: v for k, v in item.items() if k != "text"} for item in flagged]

    report = {
        "ran_at": now_utc(),
        "mode": "historical_backfill",
        "scope": {
            "after": after.isoformat().replace("+00:00", "Z") if after else None,
            "before": before.isoformat().replace("+00:00", "Z") if before else None,
            "limit": args.limit,
        },
        "messages_scanned": len(messages),
        "flagged_count": len(flagged),
        "unique_flagged_texts": len({f["fingerprint"] for f in flagged}),
        "by_code": dict(by_code.most_common()),
        "top_sessions": [
            {"session_file": session, "flagged_count": count}
            for session, count in by_session.most_common(10)
        ],
        "candidate_cases_file": str(CANDIDATES_FILE),
        "candidate_cases": len(candidates),
        "examples": report_examples[:50],
        "note": "Historical flags are discovery data. Vet candidates before adding them to the live unit cases because older transcripts may include false positives or private context.",
    }

    write_json(BACKFILL_LATEST, report)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with BACKFILL_HISTORY.open("a") as f:
        f.write(json.dumps(report, sort_keys=True) + "\n")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            "proof-gate-backfill: "
            f"scanned={report['messages_scanned']} "
            f"flagged={report['flagged_count']} "
            f"unique={report['unique_flagged_texts']} "
            f"candidates={report['candidate_cases']}"
        )
        print("by_code=" + json.dumps(report["by_code"], sort_keys=True))
        print(f"report={BACKFILL_LATEST}")
        print(f"candidates={CANDIDATES_FILE}")
    return 1 if args.fail_on_flags and flagged else 0


if __name__ == "__main__":
    raise SystemExit(main())
