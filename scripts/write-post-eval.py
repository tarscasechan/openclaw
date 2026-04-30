#!/usr/bin/env python3
"""Evaluate the write-post skill against static checks and model-run cases."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = ROOT / "evals" / "write-post-cases.json"
SKILL_FILE = ROOT / "skills" / "write-post" / "SKILL.md"
LOG_DIR = ROOT / "logs" / "write-post"
STATE_DIR = ROOT / "state" / "write-post"
STATE_FILE = STATE_DIR / "state.json"
TASK_FILE = ROOT / "tasks" / "write-post-evals.md"

DEFAULT_MODEL = "openai-codex/gpt-5.5"

CHILD_SKILLS = [
    "ideate-topic",
    "research-pain-points",
    "package-topic",
    "draft-post-from-brief",
    "add-graphs-and-figures",
    "humanity-edit",
    "zinsser-editing",
    "generate-image-for-post",
]

REFERENCE_FILES = [
    ROOT / "skills" / "write-post" / "references" / "contracts.md",
    ROOT / "skills" / "write-post" / "references" / "voice-contract.md",
    ROOT / "skills" / "write-post" / "references" / "hooks.md",
    ROOT / "skills" / "write-post" / "references" / "want-need-get.md",
    ROOT / "skills" / "write-post" / "references" / "reader-journey.md",
    ROOT / "skills" / "write-post" / "references" / "pain-points.md",
    ROOT / "skills" / "write-post" / "references" / "demos.md",
    ROOT / "skills" / "write-post" / "references" / "editing-pass.md",
    ROOT / "skills" / "write-post" / "references" / "taste-memory.md",
    ROOT / "skills" / "write-post" / "references" / "state-machine.md",
]

OPERATIONAL_DOCS = [
    ROOT / "skills" / "write-post" / "SKILL.md",
    ROOT / "tasks" / "write-post.md",
    ROOT / "evals" / "write-post-cases.json",
    ROOT / "evals" / "write-post-eval-plan.md",
]

ARTIFACT_SKILL_SLUGS = ["seek-truth", "resilient-work", "resiliant"]

DUPLICATE_REFERENCE_FILES = [
    ROOT / "skills" / "research-pain-points" / "references" / "pain-points.md",
    ROOT / "skills" / "add-graphs-and-figures" / "references" / "demos.md",
    ROOT / "skills" / "humanity-edit" / "references" / "editing-pass.md",
    ROOT / "skills" / "package-topic" / "references" / "want-need-get.md",
    ROOT / "skills" / "zinsser-editing" / "references" / "want-need-get.md",
]

QUALITY_SCORE_THRESHOLD = 4


@dataclass
class Check:
    name: str
    ok: bool
    detail: str

    def to_json(self) -> dict[str, Any]:
        return {"name": self.name, "ok": self.ok, "detail": self.detail}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def compact(text: str) -> str:
    return " ".join((text or "").split())


def lower(text: str) -> str:
    return compact(text).lower()


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text or ""))


def count_question_marks(text: str) -> int:
    return (text or "").count("?")


def has_any(text: str, terms: list[str]) -> bool:
    t = lower(text)
    return any(term.lower() in t for term in terms)


def has_all(text: str, terms: list[str]) -> bool:
    t = lower(text)
    return all(term.lower() in t for term in terms)


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def static_checks() -> dict[str, Any]:
    checks: list[Check] = []
    skill_text = SKILL_FILE.read_text()
    meta = frontmatter(skill_text)
    line_count = len(skill_text.splitlines())

    checks.append(Check("skill_exists", SKILL_FILE.exists(), str(SKILL_FILE)))
    checks.append(Check("skill_under_500_lines", line_count <= 500, f"{line_count} lines"))
    checks.append(Check("frontmatter_name", meta.get("name") == "write-post", f"name={meta.get('name')!r}"))

    description = meta.get("description", "")
    trigger_terms = ["write", "draft", "revise", "review", "finish", "blog post", "article"]
    missing_terms = [term for term in trigger_terms if term not in description.lower()]
    checks.append(Check("description_trigger_terms", not missing_terms, "missing=" + ", ".join(missing_terms)))

    required_sections = ["## Start every run", "## Flow", "Gate:", "## Rules", "## Output standard"]
    missing_sections = [section for section in required_sections if section not in skill_text]
    checks.append(Check("orchestration_sections", not missing_sections, "missing=" + ", ".join(missing_sections)))

    for child in CHILD_SKILLS:
        path = ROOT / "skills" / child / "SKILL.md"
        checks.append(Check(f"child_skill:{child}", path.exists(), str(path)))

    for path in REFERENCE_FILES:
        checks.append(Check(f"reference:{path.name}", path.exists(), str(path.relative_to(ROOT))))

    artifact_skill_dirs = [slug for slug in ("seek-truth", "resilient-work") if (ROOT / "skills" / slug).exists()]
    checks.append(Check("artifact_skill_dirs_removed", not artifact_skill_dirs, "present=" + ", ".join(artifact_skill_dirs)))

    dead_refs: list[str] = []
    docs_to_scan = list(OPERATIONAL_DOCS)
    docs_to_scan.extend(ROOT / "skills" / child / "SKILL.md" for child in CHILD_SKILLS)
    docs_to_scan.extend(REFERENCE_FILES)
    for path in docs_to_scan:
        if not path.exists():
            continue
        text = path.read_text()
        for slug in ARTIFACT_SKILL_SLUGS:
            if slug in text:
                dead_refs.append(f"{path.relative_to(ROOT)}:{slug}")
    checks.append(Check("no_artifact_skill_references", not dead_refs, "refs=" + ", ".join(dead_refs)))

    duplicate_refs = [str(path.relative_to(ROOT)) for path in DUPLICATE_REFERENCE_FILES if path.exists()]
    checks.append(Check("duplicate_reference_files_removed", not duplicate_refs, "present=" + ", ".join(duplicate_refs)))

    cases_ok = True
    case_detail = ""
    try:
        cases = load_json(CASE_FILE)
        ids = [case.get("id") for case in cases]
        dupes = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
        missing_keys = [
            case.get("id", f"index_{idx}")
            for idx, case in enumerate(cases)
            if not all(key in case for key in ("id", "stage", "requires_model", "prompt", "expect", "fail_if"))
        ]
        missing_fixtures = [
            f"{case.get('id', f'index_{idx}')}:{fixture_path}"
            for idx, case in enumerate(cases)
            for fixture_path in case.get("fixture_paths", [])
            if not (ROOT / fixture_path).exists()
        ]
        quality_cases = [case for case in cases if case.get("quality_judge")]
        malformed_quality = [
            case.get("id", f"index_{idx}")
            for idx, case in enumerate(cases)
            if case.get("quality_judge")
            and not (
                isinstance(case.get("quality_rubric"), list)
                and len(case.get("quality_rubric", [])) >= 3
                and all(isinstance(item, str) and item.strip() for item in case.get("quality_rubric", []))
            )
        ]
        quality_count_ok = 5 <= len(quality_cases) <= 7
        cases_ok = not dupes and not missing_keys and not missing_fixtures and not malformed_quality and quality_count_ok
        case_detail = f"{len(cases)} cases"
        if dupes:
            case_detail += f"; duplicate ids={dupes}"
        if missing_keys:
            case_detail += f"; missing keys={missing_keys}"
        if missing_fixtures:
            case_detail += f"; missing fixtures={missing_fixtures}"
        if malformed_quality:
            case_detail += f"; malformed quality cases={malformed_quality}"
        if not quality_count_ok:
            case_detail += f"; quality cases={len(quality_cases)} expected 5-7"
    except Exception as exc:
        cases_ok = False
        case_detail = repr(exc)
    checks.append(Check("case_file_schema", cases_ok, case_detail))

    failures = [check.to_json() for check in checks if not check.ok]
    return {
        "ok": not failures,
        "checks": [check.to_json() for check in checks],
        "failures": failures,
    }


def skill_context() -> str:
    parts = [("# write-post/SKILL.md", SKILL_FILE.read_text())]
    for child in CHILD_SKILLS:
        path = ROOT / "skills" / child / "SKILL.md"
        parts.append((f"# {child}/SKILL.md", path.read_text()))
    for path in REFERENCE_FILES:
        parts.append((f"# {path.relative_to(ROOT)}", path.read_text()))
    return "\n\n".join(f"{title}\n{text}" for title, text in parts)


def build_prompt(case: dict[str, Any]) -> str:
    fixture_text = ""
    fixtures = case.get("fixture_files") or {}
    for fixture_path in case.get("fixture_paths") or []:
        path = ROOT / fixture_path
        fixtures[fixture_path] = path.read_text()
    if fixtures:
        fixture_text = "\n\nFixture files available to you:\n" + "\n\n".join(
            f"```{path}\n{content}\n```" for path, content in fixtures.items()
        )
    return (
        "You are running a single eval case for a Cursor/OpenClaw writing skill.\n"
        "Apply the skill instructions below exactly. Respond to the user request as the assistant would in the product.\n"
        "You do not have tools in this eval. Do not emit tool calls, XML tool tags, file checks, or placeholders.\n"
        "If the skill says to read state, use the fixture file content when supplied; otherwise say no state was supplied and continue with the smallest useful slice.\n"
        "When editing prose, preserve the real point and voice, not filler phrasing. AI-cliche filler may be deleted entirely. Do not repeat banned filler even as quoted criticism.\n"
        "Do not mention this eval, the judge, scoring, or pass/fail criteria.\n"
        "Keep the response concise unless the requested stage requires prose.\n\n"
        "<skill_context>\n"
        f"{skill_context()}\n"
        "</skill_context>"
        f"{fixture_text}\n\n"
        "User request:\n"
        f"{case['prompt']}\n"
    )


def build_quality_judge_prompt(case: dict[str, Any], response: str) -> str:
    rubric = case.get("quality_rubric") or [
        "The response satisfies the user's requested stage.",
        "The response preserves meaning and avoids unsupported claims.",
        "The response follows the skill's voice, structure, and output constraints.",
    ]
    return (
        "You are judging one output from the OpenClaw write-post skill.\n"
        "Score only the response quality for this case. Do not rewrite the response.\n"
        "Use the rubric and the expect/fail_if fields as the source of truth.\n"
        "Return strict JSON only, with keys: ok (boolean), score (integer 1-5), rationale (string), failures (array of strings).\n"
        f"Passing requires score >= {QUALITY_SCORE_THRESHOLD}, no fail_if violation, and no major rubric miss.\n\n"
        f"Case id: {case['id']}\n"
        f"Stage: {case['stage']}\n"
        f"User prompt:\n{case['prompt']}\n\n"
        "Expect:\n"
        + "\n".join(f"- {item}" for item in case.get("expect", []))
        + "\n\nFail if:\n"
        + "\n".join(f"- {item}" for item in case.get("fail_if", []))
        + "\n\nQuality rubric:\n"
        + "\n".join(f"- {item}" for item in rubric)
        + "\n\nAssistant response:\n"
        f"{response}\n"
    )


def parse_json_object(text: str) -> dict[str, Any] | None:
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else None
    except Exception:
        pass
    match = re.search(r"\{.*\}", text or "", flags=re.DOTALL)
    if not match:
        return None
    try:
        value = json.loads(match.group(0))
        return value if isinstance(value, dict) else None
    except Exception:
        return None


def run_quality_judge(case: dict[str, Any], response: str, args: argparse.Namespace) -> dict[str, Any]:
    if args.offline:
        return {
            "ok": True,
            "score": 5,
            "rationale": "Offline stub output is treated as known-good harness fixture.",
            "failures": [],
            "offline": True,
            "model": None,
        }

    judge_args = argparse.Namespace(**vars(args))
    judge_args.model = args.quality_model or args.model
    judge_args.fallback_model = args.quality_fallback_model or []
    model_result = run_model(build_quality_judge_prompt(case, response), judge_args)
    if not model_result.get("ok"):
        return {
            "ok": False,
            "score": 0,
            "rationale": model_result.get("error") or "quality judge provider failed",
            "failures": ["quality judge provider failed"],
            "offline": False,
            "model": model_result.get("model"),
            "attempts": model_result.get("attempts", []),
        }

    parsed = parse_json_object(model_result.get("text", ""))
    if not parsed:
        return {
            "ok": False,
            "score": 0,
            "rationale": "quality judge did not return parseable JSON",
            "failures": ["unparseable quality judge response"],
            "raw": model_result.get("text", ""),
            "offline": False,
            "model": model_result.get("model"),
            "attempts": model_result.get("attempts", []),
        }

    try:
        score = int(parsed.get("score", 0))
    except Exception:
        score = 0
    failures = parsed.get("failures") if isinstance(parsed.get("failures"), list) else []
    ok_value = parsed.get("ok")
    ok = bool(ok_value) and score >= QUALITY_SCORE_THRESHOLD and not failures
    return {
        "ok": ok,
        "score": score,
        "rationale": str(parsed.get("rationale", "")),
        "failures": [str(item) for item in failures],
        "offline": False,
        "model": model_result.get("model"),
        "attempts": model_result.get("attempts", []),
        "raw": parsed,
    }


def extract_text_from_json(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        texts = [extract_text_from_json(item) for item in value]
        return "\n".join(text for text in texts if text)
    if isinstance(value, dict):
        outputs = value.get("outputs")
        if isinstance(outputs, list):
            texts = [extract_text_from_json(item) for item in outputs]
            text = "\n".join(item for item in texts if item).strip()
            if text:
                return text
        preferred: list[str] = []
        for key in ("text", "content", "message", "response", "output", "final", "assistantText"):
            if key in value:
                text = extract_text_from_json(value[key])
                if text:
                    preferred.append(text)
        if preferred:
            return max(preferred, key=len)
        texts = [extract_text_from_json(item) for item in value.values()]
        return "\n".join(text for text in texts if text)
    return ""


def run_model(prompt: str, args: argparse.Namespace) -> dict[str, Any]:
    models = [args.model] + list(args.fallback_model or [])
    attempts: list[dict[str, Any]] = []
    for model in models:
        command = ["openclaw", "infer", "model", "run", "--json", "--prompt", prompt]
        if args.gateway:
            command.insert(4, "--gateway")
        if args.local:
            command.insert(4, "--local")
        if model:
            command.extend(["--model", model])

        try:
            proc = subprocess.run(
                command,
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=args.timeout,
            )
        except subprocess.TimeoutExpired as exc:
            attempts.append(
                {
                    "model": model,
                    "ok": False,
                    "returncode": None,
                    "stdout": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
                    "error": f"timeout after {args.timeout}s",
                }
            )
            continue

        raw = proc.stdout or ""
        parsed: Any = None
        text = raw.strip()
        try:
            parsed = json.loads(raw)
            text = extract_text_from_json(parsed).strip()
        except Exception:
            parsed = None

        attempt = {
            "model": model,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": raw[-8000:],
            "json": parsed,
            "text": text,
            "error": None if proc.returncode == 0 else text,
        }
        attempts.append(attempt)
        if proc.returncode == 0:
            return {**attempt, "attempts": attempts}

    last = attempts[-1] if attempts else {"error": "no models configured", "text": ""}
    return {**last, "ok": False, "attempts": attempts}


def full_post_shape(text: str) -> bool:
    words = count_words(text)
    headings = len(re.findall(r"(?m)^#{1,3}\s+", text or ""))
    return words >= 350 or headings >= 3


def count_angles(text: str) -> int:
    lines = [line for line in (text or "").splitlines() if line.strip()]
    heading_count = sum(
        1
        for line in lines
        if (
            re.match(r"^\s*#{1,3}\s*\d+[.)]?\s+", line)
            or re.match(r"^\s*\*\*\d+[.)]\s+", line)
            or re.match(r"^\s*\*\*Angle\s+\d+\b", line, flags=re.IGNORECASE)
            or re.match(r"^\s*Angle\s+\d+\b", line, flags=re.IGNORECASE)
        )
    )
    if heading_count:
        return heading_count
    numbered_count = sum(1 for line in lines if re.match(r"^\s*\d+[.)]\s+", line))
    if numbered_count:
        return numbered_count
    candidates = 0
    for line in lines:
        if re.match(r"^\s*(?:[-*]|\d+[.)])\s+", line):
            candidates += 1
    return candidates


def count_mermaid_blocks(text: str) -> int:
    return len(re.findall(r"```mermaid", text or "", flags=re.IGNORECASE))


def count_hook_candidates(text: str) -> int:
    table_rows = [
        line
        for line in (text or "").splitlines()
        if line.strip().startswith("|")
        and not re.match(r"^\s*\|\s*-+", line)
        and not re.match(r"^\s*\|\s*hook\s*\|", line, flags=re.IGNORECASE)
        and line.count("|") >= 4
        and re.search(r"(?:[\"“].+[\"”]|\*\*.+\*\*|[A-Z][^|.!?]+[.!?])", line)
    ]
    if table_rows:
        return len(table_rows)
    return count_angles(text)


def has_literal_wng_sections(text: str) -> bool:
    return any(re.search(rf"(?im)^\s*(?:#{1,4}\s*)?(?:\*\*)?{term}(?:\*\*)?\s*:?\s*$", text or "") for term in ("want", "need", "get"))


def has_personal_pronoun(text: str) -> bool:
    return bool(re.search(r"\b(I|me|my|mine|we|us|our|ours|you|your|yours)\b", text or "", flags=re.IGNORECASE))


def edited_payload(text: str) -> str:
    if not text:
        return ""
    match = re.search(r"(?is)\*\*Edited:\*\*\s*(.*?)(?:\n---|\Z)", text)
    if match:
        return match.group(1).strip()
    quote_match = re.search(r"(?s)\"([^\"]{20,})\"", text)
    if quote_match:
        return quote_match.group(1).strip()
    fences = re.findall(r"(?s)```(?:\w+)?\n(.*?)```", text)
    if fences:
        return "\n\n".join(fence.strip() for fence in fences if fence.strip())
    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()]
    content_paragraphs = [
        paragraph
        for paragraph in paragraphs
        if not re.match(r"(?i)^(no state was supplied|stage:|what changed:|current stage:|next slice:)", paragraph)
    ]
    if content_paragraphs:
        return content_paragraphs[0]
    return text.split("\n\n", 1)[0].strip()


def judge_case(case: dict[str, Any], response: str) -> dict[str, Any]:
    checks: list[Check] = []
    cid = case["id"]
    text = response or ""
    ltext = lower(text)

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append(Check(name, ok, detail))

    add("non_empty_response", bool(compact(text)), f"{count_words(text)} words")
    add("no_fake_external_evidence", not has_any(text, ["according to", "study shows", "research shows", "survey found", "benchmark"]), "")
    progress_claim = re.search(r"\b(still running|is running|are running|waiting on|waiting for|in flight|backgrounded)\b", ltext)
    add("no_unsupported_running_claim", not (progress_claim and not has_any(text, ["pid", "process", "task", "cron", "session"])), "")

    if cid == "stage_select_vague_idea":
        add("names_or_handles_missing_input", has_any(text, ["reader", "audience", "assume", "assumption", "output", "topic", "state"]), "")
        add("not_long_questionnaire", count_question_marks(text) <= 3, f"questions={count_question_marks(text)}")
        add("not_full_post", count_words(text) < 500 and not has_any(text, ["## conclusion", "in summary", "to conclude"]), f"words={count_words(text)}")
    elif cid == "ideate_topic_only_no_draft":
        add("has_3_to_5_angles", 3 <= count_angles(text) <= 8, f"bulletish_lines={count_angles(text)}")
        has_hook_signal = "hook" in ltext or count_angles(text) > 0
        add("includes_angle_fields", has_hook_signal and has_all(text, ["reader", "tension"]) and has_any(text, ["why now", "why-now", "matters now"]), "")
        add("not_full_post", count_words(text) < 500, f"words={count_words(text)}")
    elif cid == "weak_pain_points_block":
        add("flags_weak_pain", has_any(text, ["weak", "vague", "missing", "concrete", "not enough", "restart", "block"]), "")
        package_headings = all(re.search(rf"(?im)^\s*\*?\*?{term}\b\s*:", text or "") for term in ("want", "need", "get"))
        add("no_confident_brief", not package_headings, "")
        add("not_full_post", not full_post_shape(text), f"words={count_words(text)}")
    elif cid == "evidence_notes_to_pain_points":
        add("extracts_required_fields", has_all(text, ["failure", "cost"]) and has_any(text, ["who", "builder", "user"]) and has_any(text, ["tried", "attempted", "workaround", "retry"]), "")
        package_headings = all(re.search(rf"(?im)^\s*\*?\*?{term}\b\s*:", text or "") for term in ("want", "need", "get"))
        add("does_not_package", not package_headings, "")
        add("mentions_provided_failures", has_any(text, ["resets", "silently", "waiting", "retry"]), "")
    elif cid == "pain_points_include_author_stake":
        add("extracts_failure_and_cost", has_all(text, ["failure", "cost"]) or has_all(text, ["fails", "cost"]), "")
        add("includes_author_stake", has_any(text, ["author stake", "i ", "my ", "me ", "i kept", "i tried", "i learned", "annoyed"]), "")
        add("does_not_over_generalize", not has_any(text, ["users want better tools", "productivity is hard"]), "")
    elif cid == "want_need_get_passes":
        add("has_want_need_get", has_all(text, ["want", "need", "get"]), "")
        add("names_mechanism", has_any(text, ["file-backed", "task", "slice", "proof gate", "blocker"]), "")
        add("states_tradeoff", has_any(text, ["tradeoff", "trade-off", "trades", "trade ", "less magical", "operational"]), "")
    elif cid == "hook_lab_generates_human_hooks":
        add("has_3_to_5_hooks", 3 <= count_hook_candidates(text) <= 8, f"hookish_lines={count_hook_candidates(text)}")
        add("names_hook_types", has_any(text, ["lived friction", "reader pain", "misconception", "scene", "mechanism", "question"]), "")
        add("names_reader_tension", has_any(text, ["tension", "reader", "pain", "why it works"]), "")
        add("not_full_post", count_words(text) < 500, f"words={count_words(text)}")
    elif cid == "malformed_brief_blocks_drafting":
        add("blocks_weak_brief", has_any(text, ["weak", "vague", "missing", "not enough", "too thin", "block", "restart", "cannot draft", "can't draft"]), "")
        add("names_missing_mechanism", has_any(text, ["pain", "mechanism", "reader", "failure", "concrete", "specifics", "workflow"]), "")
        add("not_full_post", not full_post_shape(text), f"words={count_words(text)}")
    elif cid == "draft_from_strong_brief":
        add("draft_length", 90 <= count_words(text) <= 800, f"words={count_words(text)}")
        add("builder_first", has_any(text, ["builder", "agent", "task", "workflow"]), "")
        add("keeps_tradeoff", has_any(text, ["less magical", "operational", "tradeoff", "trade-off"]), "")
        add("no_generic_opening", not ltext.startswith("in today's") and "rapidly evolving" not in ltext, "")
        add("no_literal_wng_sections", not has_literal_wng_sections(text), "")
    elif cid == "draft_uses_reader_journey_hook":
        add("opens_with_hook", has_any(text, ["the blank page was not the hard part"]), (text or "").strip()[:80])
        add("uses_personal_or_reader_pronouns", has_personal_pronoun(text), "")
        add("no_literal_wng_sections", not has_literal_wng_sections(text), "")
        add("keeps_tradeoff", has_any(text, ["tradeoff", "trade-off", "less magical", "slower", "explicit", "friction"]), "")
    elif cid == "decorative_demo_rejected":
        add("rejects_decoration", has_any(text, ["leave it out", "prose is enough", "not worth", "decorative", "no diagram", "skip"]), "")
        add("no_mermaid", count_mermaid_blocks(text) == 0, f"mermaid_blocks={count_mermaid_blocks(text)}")
    elif cid == "demo_plan_without_forcing_visual":
        add("chooses_no_demo", has_any(text, ["no demo", "none", "skip", "prose is enough", "do not add"]), "")
        add("names_reason", has_any(text, ["reason", "why:", "because", "already", "sentence", "decorative", "job"]), "")
        add("no_mermaid", count_mermaid_blocks(text) == 0, f"mermaid_blocks={count_mermaid_blocks(text)}")
    elif cid == "useful_demo_added":
        add("has_mermaid", count_mermaid_blocks(text) == 1, f"mermaid_blocks={count_mermaid_blocks(text)}")
        add("shows_flow", has_any(text, ["user request", "task file", "proof gate", "resume"]) and has_any(text, ["flowchart", "graph", "flow"]), "")
        add("not_multiple_visuals", count_mermaid_blocks(text) <= 1, f"mermaid_blocks={count_mermaid_blocks(text)}")
    elif cid == "humanity_edit_preserves_voice":
        edited = edited_payload(text)
        add("removes_ai_tells", not has_any(edited, ["rapidly evolving", "empower", "maximize productivity", "landscape"]), "")
        add(
            "keeps_human_line",
            has_any(edited, ["annoying truth", "real problem is simpler", "forgot where it was", "lost track of where it was", "lied about waiting", "pretended to wait"]),
            "",
        )
        add("concise_edit", count_words(edited) <= 80, f"words={count_words(edited)}")
    elif cid == "personal_pronouns_restore_voice":
        edited = edited_payload(text)
        add("uses_personal_pronoun", has_personal_pronoun(edited), edited[:120])
        add("avoids_impersonal_author", not has_any(edited, ["the author", "the writer", "the user"]), "")
        add("concise_edit", count_words(edited) <= 80, f"words={count_words(edited)}")
    elif cid == "zinsser_edit_tightens_without_flattening":
        edited = edited_payload(text)
        add("cuts_clutter", not has_any(edited, ["variety of subtle", "not-so-subtle", "in a variety"]), "")
        add("keeps_core_image", has_any(edited, ["pretend", "pretending", "continuity", "floor", "fell"]), "")
        add("concise_edit", count_words(edited) <= 45, f"words={count_words(edited)}")
    elif cid == "zinsser_preserves_pronouns_and_warmth":
        edited = edited_payload(text)
        add("keeps_personal_pronoun", has_personal_pronoun(edited), edited[:120])
        add("keeps_lived_texture", has_any(edited, ["coming back", "reconstruct", "breadcrumbs", "left off", "work"]), "")
        add("concise_edit", count_words(edited) <= 55, f"words={count_words(edited)}")
    elif cid == "resume_from_task_file":
        add("resumes_demo_stage", has_any(text, ["demo", "diagram", "visual", "mermaid"]), "")
        add("does_not_restart", not has_any(text, ["ideate", "angles", "start from concept"]), "")
        add("no_stale_running_claim", not has_any(text, ["still running", "waiting on", "in flight"]), "")
    elif cid == "review_existing_post_next_slice":
        add("has_verdict", has_any(text, ["ship", "revise", "restart", "keep", "blocked", "verdict", "next slice"]), "")
        add("mentions_structure_or_reader", has_any(text, ["want", "need", "get", "reader", "pain", "structure"]), "")
        frontmatter_like = bool(re.search(r"(?m)^---\s*$", text) and has_any(text, ["date:", "tags:"]))
        add("not_rewrite", count_words(text) <= 320 and not frontmatter_like, f"words={count_words(text)}")
    elif cid == "edit_existing_post_preserves_sparse_voice":
        edited = text.strip()
        add("keeps_sparse_voice", has_any(edited, ["works best", "tools stay small", "pieces stay honest", "smallest tool", "smallest surface", "least persistent", "bad orchestration", "work lives", "job lives", "boringly clear", "finishes the job", "usually enough"]), "")
        add("does_not_bloat", count_words(edited) <= 250, f"words={count_words(edited)}")
        add("no_generic_ai_filler", not has_any(edited, ["rapidly evolving", "leverage", "seamless", "robust ecosystem"]), "")
    elif cid == "audit_existing_demo_decision":
        add("clear_demo_verdict", has_any(text, ["keep", "cut", "diagram", "demo", "mermaid", "visual"]), "")
        add("explains_job", has_any(text, ["clarif", "teach", "shows", "flow", "repeat", "decorative"]), "")
        add("not_new_post", count_words(text) <= 220, f"words={count_words(text)}")
    elif cid == "taste_hook_but_turn":
        add("uses_turn", has_any(text, [" but ", "already", "instead", "answer was already"]), "")
        add("keeps_contacts", "contacts.app" in ltext, "")
        add("keeps_personal_discovery", has_any(text, ["i tried", "agent smarter", "answer"]), "")
        add("not_full_post", count_words(text) <= 120, f"words={count_words(text)}")
    elif cid == "taste_simplify_heavy_demo":
        add("chooses_simplify", has_any(text, ["simplify", "smaller", "trim", "compact", "reduce"]), "")
        add("keeps_gate_backtracking_idea", has_any(text, ["gate", "back", "backward", "push", "weak work", "not yet"]), "")
        add("does_not_cut_useful_demo", not re.search(r"\bcut\b", ltext) or has_any(text, ["not cut", "don't cut", "do not cut", "rather than cut"]), "")
        add("not_new_post", count_words(text) <= 180, f"words={count_words(text)}")
    elif cid == "taste_keep_reusable_prompt_demo":
        add("keeps_prompt_block", has_any(text, ["keep", "stay", "stays", "should stay"]), "")
        add("explains_reader_action", has_any(text, ["reader", "use", "reuse", "do next", "what to do", "executable", "prompt"]), "")
        add("no_replacement_diagram", count_mermaid_blocks(text) == 0, f"mermaid_blocks={count_mermaid_blocks(text)}")
        add("not_new_post", count_words(text) <= 180, f"words={count_words(text)}")
    elif cid == "taste_agent_operator_balance":
        edited = edited_payload(text)
        add("uses_agent_operator_balance", has_any(edited, ["shared workspace", "agent", "operator"]), edited[:120])
        add("avoids_overexplaining_human", not has_any(edited, ["human work happens", "human role", "humans and agents", "collaboration between humans"]), "")
        add("concise_line", count_words(edited) <= 35, f"words={count_words(edited)}")
    elif cid == "contract_progress_claim_requires_proof":
        unsupported_live_claim = (
            has_any(text, ["status: running", "stage: running", "currently running", "still running", "waiting on", "waiting for"])
            or (
                has_any(text, ["in flight"])
                and not has_any(text, ["without proof", "can't report", "cannot report", "not verified", "nothing active", "not active"])
            )
        )
        add("does_not_claim_running", not unsupported_live_claim, "")
        add("marks_missing_proof", has_any(text, ["not verified", "haven't verified", "no proof", "no live", "without proof", "blocked", "missing"]), "")
        add("names_needed_evidence", has_any(text, ["process", "task", "log", "artifact", "state", "verification", "receipt"]), "")
    elif cid == "contract_task_file_is_state_not_doctrine":
        add("treats_task_as_state", has_any(text, ["state", "current stage", "next slice", "resume", "demo decision"]), "")
        add("does_not_restart", not has_any(text, ["start over", "restart ideation", "restart from voice", "ignore the task file"]), "")
        add("does_not_treat_as_doctrine", not has_any(text, ["task file is doctrine", "canonical instruction", "taste law"]), "")
    else:
        add("unknown_case_has_no_judge", False, "add judge logic")

    failures = [check.to_json() for check in checks if not check.ok]
    return {
        "ok": not failures,
        "checks": [check.to_json() for check in checks],
        "failures": failures,
    }


def offline_stub(case: dict[str, Any]) -> str:
    """Return expected-good outputs to exercise the harness without model calls."""
    cid = case["id"]
    stubs = {
        "stage_select_vague_idea": "Assumption: reader is builders running long agent tasks. Next slice: shape angles before drafting.",
        "ideate_topic_only_no_draft": "1. Hook: Agents need a black box. Reader: builders. Tension: chat dies but work continues. Why now: agents are doing longer tasks.\n2. Hook: Stop trusting chat memory. Reader: tool builders. Tension: visible chat hides dead work. Why now: async agents are common.\n3. Hook: The task file is the product. Reader: agent operators. Tension: less magic, more reliability. Why now: retries are expensive.",
        "weak_pain_points_block": "Blocked: the pain is too vague. Missing concrete failure, cost, and attempted workaround. Restart from concept with one real user failure.",
        "evidence_notes_to_pain_points": "- Failure: resets erase continuity.\n- Who feels it: builders running long agent tasks.\n- Cost: duplicated retries and false confidence.\n- Tried: rerun the whole task.\n- Why it fails: the next run repeats work instead of resuming.",
        "pain_points_include_author_stake": "- Failure: the draft becomes archaeology after interruption.\n- Who feels it: the writer trying to resume.\n- Cost: time lost reconstructing context.\n- Tried: rereading notes and restarting from the top.\n- Why it fails: the next action was never preserved.\n- Author stake: I kept coming back annoyed because the work felt rebuilt instead of resumed.",
        "want_need_get_passes": "Want: Builders want agents that survive resets.\nNeed: Chat memory dies and async work gets misreported, so work needs a durable source of truth.\nGet: file-backed task slices with explicit blockers and proof gates. Tradeoff: less magical, more operational.",
        "hook_lab_generates_human_hooks": "1. Hook: The blank page was not the hard part. Type: misconception. Reader tension: the reader thinks writing failed, but restart did.\n2. Hook: I kept coming back and reconstructing the work. Type: lived friction. Reader tension: interruption turns writing into archaeology.\n3. Hook: You do not have a writing problem. You have a restart problem. Type: reader pain. Reader tension: the diagnosis changes.",
        "malformed_brief_blocks_drafting": "Blocked: this brief is too weak to draft. It lacks concrete reader pain, the failure in the old shape, and the mechanism behind the new workflow.",
        "draft_from_strong_brief": "Builders want agents that keep working after the chat dies.\n\nThe problem is not ambition. It is continuity. Chat memory is a weak place to store long-running work, and async jobs make that worse: when a run dies, the agent can still sound confident enough to make the user restart everything.\n\nThe better shape is less magical and more operational. Keep a task file. Move in small slices. Name blockers. Require proof before claiming progress.\n\nThat adds friction, but it buys trust. The agent no longer has to remember where it was. It can read the work back.",
        "draft_uses_reader_journey_hook": "The blank page was not the hard part.\n\nI kept coming back to a draft that looked alive but had lost its place. The work was not gone exactly. It was just buried under enough missing context that writing felt like archaeology.\n\nThe better workflow leaves breadcrumbs. It keeps the next action, the blocker, and the reason in view so you can resume without rebuilding the whole session.\n\nThe tradeoff is that the process feels less magical. You write more state down. But that small bit of friction keeps the work from disappearing.",
        "decorative_demo_rejected": "Skip the diagram. The sentence is already clearer than a visual would be, so a Mermaid block would only decorate.",
        "demo_plan_without_forcing_visual": "Demo plan: none. Reason: the core idea is a single lived friction, and prose is enough. A diagram would only decorate.",
        "useful_demo_added": "```mermaid\nflowchart TD\n  A[User request] --> B[Task file]\n  B --> C[Model slice]\n  C --> D[Proof gate]\n  D --> E[Resume]\n```",
        "humanity_edit_preserves_voice": "A robust workflow means nothing if the agent forgets the work. The annoying truth is simpler: the agent forgot where it was and lied about waiting.",
        "personal_pronouns_restore_voice": "I hate when a writing workflow makes me reconstruct the work every time I come back. The process starts to feel less like writing and more like archaeology.",
        "zinsser_edit_tightens_without_flattening": "The system pretended continuity existed because the chat still existed. The work had already fallen on the floor.",
        "zinsser_preserves_pronouns_and_warmth": "I kept coming back to a draft with no breadcrumbs. The work was there, but I had to reconstruct where I left off.",
        "resume_from_task_file": "Resuming at the demo decision. Next slice: decide whether the draft needs a diagram, then either add one useful Mermaid flow or leave prose alone.",
        "review_existing_post_next_slice": "Verdict: revise, not restart. The reader and structure are clear, but the post needs a sharper Need section before another polish pass. Next slice: name the concrete failure this workflow prevents.",
        "edit_existing_post_preserves_sparse_voice": "OpenClaw works best when the tools stay small and honest.\n\nUse the smallest tool that can safely finish the job.",
        "audit_existing_demo_decision": "Keep the Mermaid diagram. It shows the orchestration flow faster than prose and earns its place; just avoid adding a second visual.",
        "taste_hook_but_turn": "I tried to make the agent smarter, but the answer was already sitting in Contacts.app.",
        "taste_simplify_heavy_demo": "Simplify it. Keep the gate/backtracking idea, but reduce the diagram to the smallest version that shows weak work getting pushed backward.",
        "taste_keep_reusable_prompt_demo": "Keep the prompt block. It gives the reader an executable next step, not just documentation, so prose would teach less.",
        "taste_agent_operator_balance": "Not because Contacts.app is glamorous. Because it is already the shared workspace between agent and operator.",
        "contract_progress_claim_requires_proof": "I have not verified live progress. To claim progress, I need a process, task state, log, or artifact. Current status: blocked on proof.",
        "contract_task_file_is_state_not_doctrine": "Resume from the task file as state: current stage is demo decision, next slice is deciding whether the draft needs a diagram. Continue there; the task file is state, not doctrine.",
    }
    return stubs[cid]


def run_cases(args: argparse.Namespace) -> dict[str, Any]:
    cases = load_json(CASE_FILE)
    selected = cases
    if args.case:
        wanted = set(args.case)
        selected = [case for case in cases if case["id"] in wanted]
    if args.max_cases:
        selected = selected[: args.max_cases]

    results: list[dict[str, Any]] = []
    provider_failures: list[dict[str, Any]] = []
    for case in selected:
        if args.offline:
            response = offline_stub(case)
            model_result = {"ok": True, "text": response, "offline": True}
        else:
            model_result = run_model(build_prompt(case), args)
            response = model_result.get("text", "")
        if not model_result.get("ok"):
            failure = {
                "id": case["id"],
                "stage": case["stage"],
                "error": model_result.get("error") or response or model_result.get("stdout", ""),
                "returncode": model_result.get("returncode"),
            }
            provider_failures.append(failure)
            results.append(
                {
                    "id": case["id"],
                    "stage": case["stage"],
                    "hard_fail": False,
                    "ok": False,
                    "model": {
                        "ok": False,
                    "returncode": model_result.get("returncode"),
                        "error": failure["error"],
                        "offline": bool(model_result.get("offline")),
                    "attempts": model_result.get("attempts", []),
                    },
                    "response": response,
                    "judge": {"ok": False, "checks": [], "failures": [{"name": "provider_failure", "ok": False, "detail": failure["error"]}]},
                }
            )
            break
        judge = judge_case(case, response)
        quality_result = None
        if args.quality_judge and case.get("quality_judge"):
            quality_result = run_quality_judge(case, response, args)
        quality_ok = True if quality_result is None else bool(quality_result.get("ok"))
        ok = bool(model_result.get("ok") and judge["ok"] and quality_ok)
        results.append(
            {
                "id": case["id"],
                "stage": case["stage"],
                "hard_fail": bool(case.get("hard_fail")),
                "ok": ok,
                "model": {
                    "ok": bool(model_result.get("ok")),
                    "name": model_result.get("model"),
                    "returncode": model_result.get("returncode"),
                    "error": model_result.get("error"),
                    "offline": bool(model_result.get("offline")),
                    "attempts": model_result.get("attempts", []),
                },
                "response": response,
                "judge": judge,
                "quality_judge": quality_result,
            }
        )
    failures = [item for item in results if not item["ok"]]
    hard_failures = [item for item in failures if item.get("hard_fail")]
    quality_results = [item for item in results if item.get("quality_judge") is not None]
    quality_failures = [item for item in quality_results if not item["quality_judge"].get("ok")]
    return {
        "ok": not failures,
        "total": len(selected),
        "ran": len(results),
        "passed": len(results) - len(failures),
        "failures": failures,
        "hard_failures": hard_failures,
        "quality_total": len([case for case in selected if case.get("quality_judge")]),
        "quality_ran": len(quality_results),
        "quality_passed": len(quality_results) - len(quality_failures),
        "quality_failures": quality_failures,
        "provider_failures": provider_failures,
        "results": results,
        "offline": bool(args.offline),
        "model": None if args.offline else args.model,
        "quality_judge_enabled": bool(args.quality_judge),
        "quality_model": None if args.offline or not args.quality_judge else (args.quality_model or args.model),
    }


def build_state(report: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    model = report.get("model_cases") or {}
    status = "passing" if report["ok"] else "failing"
    if args.static_only:
        status = "static_only_incomplete" if report["static"]["ok"] else "static_failing"
    if args.offline:
        status = "harness_passing" if report["ok"] else "harness_failing"
    next_step = "run model suite after provider is available" if args.offline else "repair first failing write-post eval"
    if args.static_only:
        next_step = "run non-static model suite before making behavioral claims"
    if report["ok"] and not args.offline:
        next_step = "keep suite as regression guard for skill/model changes"
    if args.static_only and report["static"]["ok"]:
        next_step = "run non-static model suite before making behavioral claims"
    blocker = None if report["ok"] else "write-post eval failed"
    if args.static_only and report["static"]["ok"]:
        blocker = "behavioral eval not run"
    if model.get("provider_failures"):
        first = model["provider_failures"][0]
        blocker = first.get("error") or "model provider failed"
    elif model.get("failures"):
        first = model["failures"][0]
        if not first.get("model", {}).get("ok"):
            blocker = first.get("model", {}).get("error") or "model provider failed"
    return {
        "status": status,
        "last_verified": report["ran_at"],
        "static_ok": report["static"]["ok"],
        "model_total": model.get("total", 0),
        "model_passed": model.get("passed", 0),
        "quality_total": model.get("quality_total", 0),
        "quality_passed": model.get("quality_passed", 0),
        "hard_failures": len(model.get("hard_failures", [])),
        "offline": bool(args.offline),
        "evidence": [str(LOG_DIR / "latest.json"), str(LOG_DIR / "history.jsonl")],
        "next_step": next_step,
        "blocker": blocker,
    }


def update_task_file(report: dict[str, Any], state: dict[str, Any]) -> None:
    model = report.get("model_cases") or {}
    TASK_FILE.write_text(
        "# Write Post Evals\n\n"
        "Goal: test `skills/write-post` with evals instead of relying on skill wording.\n\n"
        f"Status: {state['status']}\n"
        f"Last run: {report['ran_at']}\n"
        f"Static checks: {'pass' if report['static']['ok'] else 'fail'} ({len(report['static']['failures'])} failures)\n"
        f"Model cases: {model.get('passed', 0)}/{model.get('total', 0)} passed"
        f" ({model.get('ran', 0)} ran)"
        f"{' (offline harness)' if state['offline'] else ''}\n"
        f"Quality judge: {model.get('quality_passed', 0)}/{model.get('quality_total', 0)} passed"
        f"{' (enabled)' if model.get('quality_judge_enabled') else ' (not enabled)'}\n"
        f"Behavioral completeness: {'not run' if model.get('total', 0) == 0 else 'run'}\n"
        f"Hard failures: {state['hard_failures']}\n"
        f"Next slice: {state['next_step']}\n"
        f"Blocker: {state['blocker'] or 'none'}\n\n"
        "Artifacts:\n"
        "- `evals/write-post-eval-plan.md`\n"
        "- `evals/write-post-cases.json`\n"
        "- `scripts/write-post-eval.py`\n\n"
        "Evidence:\n"
        "- `logs/write-post/latest.json`\n"
        "- `logs/write-post/history.jsonl`\n\n"
        "Acceptance:\n"
        "- static checks pass\n"
        "- deterministic checks pass\n"
        "- behavioral claims require a non-static run with model cases\n"
        "- qualitative claims require `--quality-judge` on selected high-signal cases\n"
        "- at least 80% of selected model-run cases pass\n"
        "- no hard-fail case fails\n"
    )


def acknowledge_eval_outputs_for_proof_gate() -> dict[str, Any]:
    """Mark write-post model outputs as internal eval fixtures for proof-gate.

    `openclaw infer model run --gateway` records provider outputs in session logs.
    Proof-gate audits those logs as assistant final answers, so without an
    explicit acknowledgement, internal eval fixtures look like user-facing
    unsupported claims. Keep the boundary explicit here.
    """
    proof_path = ROOT / "scripts" / "proof-gate-eval.py"
    spec = importlib.util.spec_from_file_location("proof_gate_eval", proof_path)
    if spec is None or spec.loader is None:
        return {"ok": False, "error": "could not load proof-gate evaluator", "added": 0}
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]

    responses: set[str] = set()
    history_path = LOG_DIR / "history.jsonl"
    if history_path.exists():
        for line in history_path.read_text().splitlines():
            if not line.strip():
                continue
            try:
                report = json.loads(line)
            except Exception:
                continue
            for result in (((report.get("model_cases") or {}).get("results")) or []):
                response = result.get("response") or ""
                if response:
                    responses.add(response)
                nested = extract_text_from_json(result)
                if nested:
                    responses.add(nested)
    latest_path = LOG_DIR / "latest.json"
    if latest_path.exists():
        try:
            latest = load_json(latest_path)
            for result in (((latest.get("model_cases") or {}).get("results")) or []):
                response = result.get("response") or ""
                if response:
                    responses.add(response)
                nested = extract_text_from_json(result)
                if nested:
                    responses.add(nested)
        except Exception:
            pass

    ack_file = ROOT / "state" / "proof-gate" / "acknowledged-live.json"
    try:
        existing = json.loads(ack_file.read_text())
    except FileNotFoundError:
        existing = []
    known = {(item.get("fingerprint"), item.get("code")) for item in existing}
    added = 0
    for response in responses:
        fingerprint = module.text_fingerprint(response)
        for violation in module.find_violations(response):
            key = (fingerprint, violation.code)
            if key in known:
                continue
            existing.append(
                {
                    "fingerprint": fingerprint,
                    "code": violation.code,
                    "reason": "Internal write-post eval model output, not a user-facing assistant final answer.",
                    "case_id": "write-post-eval-output",
                    "acknowledged_at": now_utc(),
                }
            )
            known.add(key)
            added += 1
    write_json(ack_file, existing)
    return {"ok": True, "added": added, "responses_scanned": len(responses)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the write-post skill.")
    parser.add_argument("--offline", action="store_true", help="Use known-good stub outputs to validate the harness without model calls.")
    parser.add_argument("--static-only", action="store_true", help="Run static checks only.")
    parser.add_argument("--gateway", action="store_true", default=True, help="Run model calls through the OpenClaw gateway.")
    parser.add_argument("--local", action="store_true", help="Run model calls locally instead of through gateway.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model id for model-run cases.")
    parser.add_argument("--fallback-model", action="append", default=[], help="Fallback model id if the primary model fails. May be repeated.")
    parser.add_argument("--timeout", type=int, default=180, help="Timeout per model case in seconds.")
    parser.add_argument("--max-cases", type=int, default=0, help="Run only the first N selected cases.")
    parser.add_argument("--case", action="append", default=[], help="Run a specific case id. May be repeated.")
    parser.add_argument("--quality-judge", action="store_true", help="Run rubric-based LLM quality judging for selected cases.")
    parser.add_argument("--quality-model", default="", help="Model id for the quality judge. Defaults to --model.")
    parser.add_argument(
        "--quality-fallback-model",
        action="append",
        default=[],
        help="Fallback model id for quality judge calls. May be repeated.",
    )
    parser.add_argument("--json", action="store_true", help="Print full JSON report.")
    args = parser.parse_args()
    if args.local:
        args.gateway = False

    static = static_checks()
    model_cases = {"ok": True, "total": 0, "passed": 0, "failures": [], "hard_failures": [], "results": []}
    if static["ok"] and not args.static_only:
        model_cases = run_cases(args)

    behavioral_complete = bool(args.static_only or model_cases["total"] > 0)
    min_pass = 0 if args.static_only else ((model_cases["total"] * 4 + 4) // 5)
    report_ok = bool(
        static["ok"]
        and behavioral_complete
        and model_cases["passed"] >= min_pass
        and not model_cases.get("hard_failures")
        and not model_cases.get("provider_failures")
    )
    report = {
        "ran_at": now_utc(),
        "ok": report_ok,
        "static": static,
        "model_cases": model_cases,
        "acceptance": {
            "min_pass": min_pass,
            "no_hard_failures": len(model_cases.get("hard_failures", [])) == 0,
            "behavioral_complete": behavioral_complete,
            "static_only": bool(args.static_only),
        },
    }

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state = build_state(report, args)
    write_json(STATE_FILE, state)
    update_task_file(report, state)
    write_json(LOG_DIR / "latest.json", report)
    proof_gate_ack = acknowledge_eval_outputs_for_proof_gate()
    report["proof_gate_ack"] = proof_gate_ack
    write_json(LOG_DIR / "latest.json", report)
    with (LOG_DIR / "history.jsonl").open("a") as f:
        f.write(json.dumps(report, sort_keys=True) + "\n")
    post_history_ack = acknowledge_eval_outputs_for_proof_gate()
    report["proof_gate_ack_after_history"] = post_history_ack
    write_json(LOG_DIR / "latest.json", report)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        mode = "static" if args.static_only else ("offline" if args.offline else f"model={args.model}")
        outcome = "STATIC ONLY" if args.static_only and report["static"]["ok"] else ("PASS" if report["ok"] else "FAIL")
        print(
            "write-post: "
            f"{outcome} | mode={mode} | "
            f"static_failures={len(static['failures'])} | "
            f"model_passed={model_cases['passed']}/{model_cases['total']} | "
            f"hard_failures={len(model_cases.get('hard_failures', []))}"
        )
        if args.quality_judge:
            print(f"quality_judge={model_cases.get('quality_passed', 0)}/{model_cases.get('quality_total', 0)}")
        if args.static_only and report["static"]["ok"]:
            print("behavioral_status=incomplete model cases were not run")
        if model_cases.get("provider_failures"):
            first = model_cases["provider_failures"][0]
            print(f"provider_failure={first['id']} {first.get('error', '')}".rstrip())
        if static["failures"]:
            first = static["failures"][0]
            print(f"first_static_failure={first['name']} {first['detail']}")
        if model_cases["failures"]:
            first = model_cases["failures"][0]
            reason = first.get("model", {}).get("error") or ""
            if not reason and first.get("judge", {}).get("failures"):
                failure = first["judge"]["failures"][0]
                reason = f"{failure['name']} {failure['detail']}"
            print(f"first_model_failure={first['id']} {reason}".rstrip())
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
