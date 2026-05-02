#!/usr/bin/env python3
"""Evaluate durable course-planning agent packs.

Default behavior runs static pack checks. If --outputs-dir is supplied, also
scores saved smoke-test outputs at <outputs-dir>/<case-id>/<agent>.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def resolve_path(root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    return path if path.is_absolute() else root / path


def display_path(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def no_private_paths(text: str) -> bool:
    private_markers = ["/Users/", "~/.openclaw", "credentials/", "auth-profiles.json"]
    return not any(marker in text for marker in private_markers)


def check_agent_pack(root: Path, agent_id: str, spec: dict[str, Any]) -> list[Check]:
    pack_dir = root / spec["packDir"]
    checks: list[Check] = []
    checks.append(Check(f"agent:{agent_id}:pack_dir", pack_dir.is_dir(), spec["packDir"]))

    combined = ""
    readable_files: dict[str, str] = {}
    for rel in spec.get("requiredFiles", []):
        path = pack_dir / rel
        ok = path.is_file()
        checks.append(Check(f"agent:{agent_id}:file:{rel}", ok, f"{spec['packDir']}/{rel}"))
        if ok and path.suffix.lower() in {".md", ".txt"}:
            text = read_text(path)
            readable_files[rel] = text
            combined += "\n" + text

    if combined:
        checks.append(Check(f"agent:{agent_id}:no_private_paths", no_private_paths(combined)))
    else:
        checks.append(Check(f"agent:{agent_id}:no_private_paths", False, "no readable files"))

    agent_card = readable_files.get("agent.md", "")
    checks.append(Check(f"agent:{agent_id}:pi_card", "Runtime target: Pi-compatible agent loop" in agent_card))
    checks.append(Check(f"agent:{agent_id}:model_class", "Model class:" in agent_card))
    checks.append(Check(f"agent:{agent_id}:tool_manifest", "Required tools:" in agent_card and "Optional tools:" in agent_card))

    openclaw_adapter = readable_files.get("AGENTS.md", "")
    checks.append(Check(f"agent:{agent_id}:openclaw_adapter", "OpenClaw Adapter" in openclaw_adapter and "agent.md" in openclaw_adapter))

    for phrase in spec.get("requiredPhrases", []):
        checks.append(Check(f"agent:{agent_id}:phrase:{phrase}", phrase in combined))

    return checks


def section_present(text: str, section: str) -> bool:
    # Accept exact labels like `Cut list:` and combined labels like
    # `Cut list / next courses:` when the case asks for `Cut list`.
    pattern = rf"(^|\n)\s*(#{1,4}\s*)?\**{re.escape(section)}\**\s*([^\n:]*:|\s*$)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def lesson_count(text: str) -> int:
    patterns = [
        r"(?im)^\s*#{1,4}\s*Lesson\s+\d+\b",
        r"(?im)^\s*\d+\.\s+\**Lesson\s+\d+\b",
        r"(?im)^\s*Lesson\s+\d+\s*[:—-]",
    ]
    count = max(len(re.findall(pattern, text)) for pattern in patterns)
    if count:
        return count

    # Strategic Lesson Loom outputs often list the lesson spine as numbered
    # verb-led items under `Lesson spine:` rather than headings named Lesson N.
    match = re.search(r"(?ims)^\s*(#{1,4}\s*)?\**Lesson spine\**\s*:[ \t]*\n(?P<body>.*?)(?=^\s*(#{1,4}\s*)?\**(?:Eval path|Cut list|Placement)\b)", text)
    if match:
        return len(re.findall(r"(?m)^\s*\d+\.\s+", match.group("body")))

    return 0


def count_but_hooks(text: str) -> int:
    return len(re.findall(r"(?im)^\s*(\*\*)?But\b", text))


def score_output(root: Path, case: dict[str, Any], output_path: Path) -> list[Check]:
    checks: list[Check] = []
    case_id = case["id"]
    if not output_path.is_file():
        return [Check(f"case:{case_id}:output_exists", False, display_path(root, output_path))]

    text = read_text(output_path)
    checks.append(Check(f"case:{case_id}:output_exists", True, display_path(root, output_path)))
    checks.append(Check(f"case:{case_id}:no_private_paths", no_private_paths(text)))

    for section in case.get("requiredSections", []):
        checks.append(Check(f"case:{case_id}:section:{section}", section_present(text, section)))

    low, high = case.get("lessonRange", [0, 999])
    lessons = lesson_count(text)
    checks.append(Check(f"case:{case_id}:lesson_count", low <= lessons <= high, f"found {lessons}, expected {low}-{high}"))

    if case.get("requiresButHooks"):
        buts = count_but_hooks(text)
        checks.append(Check(f"case:{case_id}:but_hooks", buts >= lessons and lessons > 0, f"lessons={lessons}, but_hooks={buts}"))

    for phrase in case.get("requiredPhrases", []):
        checks.append(Check(f"case:{case_id}:phrase:{phrase}", phrase.lower() in text.lower()))

    return checks


def summarize_checks(checks: list[Check]) -> dict[str, Any]:
    failed = [check for check in checks if not check.ok]
    return {
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "total": len(checks),
    }


def render_markdown_report(checks: list[Check], args: argparse.Namespace, generated_at: str) -> str:
    summary = summarize_checks(checks)
    lines = [
        "# Agent Pack Eval Report",
        "",
        f"Generated: {generated_at}",
        f"Cases: `{args.cases}`",
        f"Outputs dir: `{args.outputs_dir or 'not supplied'}`",
        "",
        f"Summary: passed={summary['passed']} failed={summary['failed']} total={summary['total']}",
        "",
        "## Checks",
        "",
    ]

    for check in checks:
        status = "PASS" if check.ok else "FAIL"
        detail = f" - {check.detail}" if check.detail else ""
        lines.append(f"- {status} `{check.name}`{detail}")

    lines.append("")
    return "\n".join(lines)


def write_report(root: Path, checks: list[Check], args: argparse.Namespace) -> dict[str, str]:
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    report_dir = resolve_path(root, args.report_dir)
    if report_dir is None:
        raise ValueError("--report-dir could not be resolved")
    report_dir.mkdir(parents=True, exist_ok=True)

    summary = summarize_checks(checks)
    payload = {
        "generatedAt": generated_at,
        "cases": args.cases,
        "outputsDir": args.outputs_dir,
        **summary,
        "checks": [check.__dict__ for check in checks],
    }

    latest_json = report_dir / "latest.json"
    latest_md = report_dir / "latest.md"
    history_jsonl = report_dir / "history.jsonl"

    latest_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest_md.write_text(render_markdown_report(checks, args, generated_at), encoding="utf-8")
    with history_jsonl.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")

    return {
        "json": str(latest_json.relative_to(root)),
        "markdown": str(latest_md.relative_to(root)),
        "history": str(history_jsonl.relative_to(root)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", default="evals/agent-course-cases.json")
    parser.add_argument("--outputs-dir", default=None)
    parser.add_argument("--report-dir", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    cases_path = resolve_path(root, args.cases)
    if cases_path is None:
        raise ValueError("--cases is required")
    spec = load_json(cases_path)
    checks: list[Check] = []

    for agent_id, agent_spec in spec.get("agents", {}).items():
        checks.extend(check_agent_pack(root, agent_id, agent_spec))

    if args.outputs_dir:
        outputs_dir = resolve_path(root, args.outputs_dir)
        if outputs_dir is None:
            raise ValueError("--outputs-dir could not be resolved")
        for case in spec.get("cases", []):
            path = outputs_dir / case["id"] / f"{case['agent']}.md"
            checks.extend(score_output(root, case, path))

    report_paths = write_report(root, checks, args) if args.report_dir else None
    summary = summarize_checks(checks)
    passed = summary["passed"]
    failed = [check for check in checks if not check.ok]

    if args.json:
        print(json.dumps(
            {
                **summary,
                "reportPaths": report_paths,
                "checks": [check.__dict__ for check in checks],
            },
            indent=2,
        ))
    else:
        for check in checks:
            status = "PASS" if check.ok else "FAIL"
            detail = f" — {check.detail}" if check.detail else ""
            print(f"{status} {check.name}{detail}")
        print(f"\nSUMMARY passed={passed} failed={len(failed)}")
        if report_paths:
            print(f"REPORT {report_paths['markdown']}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
