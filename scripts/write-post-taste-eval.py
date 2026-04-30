#!/usr/bin/env python3
"""Build a human-in-the-loop taste review packet from existing posts."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POST_DIR = ROOT / "_posts"
RUBRIC_FILE = ROOT / "evals" / "write-post-taste-rubric.json"
LOG_DIR = ROOT / "logs" / "write-post-taste"
TASK_FILE = ROOT / "tasks" / "write-post-taste.md"
DEFAULT_MODEL = "openai-codex/gpt-5.5"


@dataclass
class Candidate:
    id: str
    post: str
    title: str
    category_id: str
    excerpt: str
    line_start: int
    line_end: int
    reason: str
    heuristic_score: int

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "post": self.post,
            "title": self.title,
            "category_id": self.category_id,
            "excerpt": self.excerpt,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "reason": self.reason,
            "heuristic_score": self.heuristic_score,
        }


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def compact(text: str) -> str:
    return " ".join((text or "").split())


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text or ""))


def parse_post(path: Path) -> dict[str, Any]:
    text = path.read_text()
    metadata: dict[str, str] = {}
    body_start = 1
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            front = text[4:end].strip()
            for line in front.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip().strip('"')
            body = text[end + 4 :]
            body_start = text[: end + 4].count("\n") + 1
    lines = body.splitlines()
    return {
        "path": path,
        "relative_path": str(path.relative_to(ROOT)),
        "title": metadata.get("title") or path.stem,
        "body": body,
        "lines": lines,
        "body_start": body_start,
    }


def paragraphs(post: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    current: list[str] = []
    start_line = post["body_start"]
    for idx, line in enumerate(post["lines"], start=post["body_start"]):
        if not line.strip():
            if current:
                items.append({"text": "\n".join(current).strip(), "start": start_line, "end": idx - 1})
                current = []
            continue
        if not current:
            start_line = idx
        current.append(line)
    if current:
        items.append({"text": "\n".join(current).strip(), "start": start_line, "end": post["body_start"] + len(post["lines"]) - 1})
    return items


def sections(post: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    current_heading = "Opening"
    current: list[str] = []
    start_line = post["body_start"]
    for idx, line in enumerate(post["lines"], start=post["body_start"]):
        if line.startswith("## "):
            if current:
                result.append({"heading": current_heading, "text": "\n".join(current).strip(), "start": start_line, "end": idx - 1})
            current_heading = line.lstrip("#").strip()
            current = [line]
            start_line = idx
        else:
            if not current:
                start_line = idx
            current.append(line)
    if current:
        result.append({"heading": current_heading, "text": "\n".join(current).strip(), "start": start_line, "end": post["body_start"] + len(post["lines"]) - 1})
    return result


def add_candidate(candidates: list[Candidate], post: dict[str, Any], category_id: str, excerpt: str, start: int, end: int, reason: str, score: int) -> None:
    cleaned = excerpt.strip()
    if not cleaned or count_words(cleaned) < 3:
        return
    cid = f"c{len(candidates) + 1:03d}"
    candidates.append(
        Candidate(
            id=cid,
            post=post["relative_path"],
            title=post["title"],
            category_id=category_id,
            excerpt=cleaned,
            line_start=start,
            line_end=end,
            reason=reason,
            heuristic_score=score,
        )
    )


def extract_fences(post: dict[str, Any]) -> list[dict[str, Any]]:
    fences: list[dict[str, Any]] = []
    in_fence = False
    start = post["body_start"]
    buffer: list[str] = []
    for idx, line in enumerate(post["lines"], start=post["body_start"]):
        if line.startswith("```"):
            if not in_fence:
                in_fence = True
                start = idx
                buffer = [line]
            else:
                buffer.append(line)
                fences.append({"text": "\n".join(buffer), "start": start, "end": idx})
                in_fence = False
                buffer = []
        elif in_fence:
            buffer.append(line)
    return fences


def extract_candidates(posts: list[dict[str, Any]]) -> list[Candidate]:
    candidates: list[Candidate] = []
    for post in posts:
        paras = [p for p in paragraphs(post) if not p["text"].startswith("---")]
        if paras:
            opening = "\n\n".join(p["text"] for p in paras[:2])
            add_candidate(candidates, post, "hook_truth_vs_cleverness", opening, paras[0]["start"], paras[min(1, len(paras) - 1)]["end"], "Opening determines whether the post invites or merely announces.", 8)
            ending = "\n\n".join(p["text"] for p in paras[-2:])
            add_candidate(candidates, post, "ending_quality", ending, paras[-2]["start"] if len(paras) > 1 else paras[-1]["start"], paras[-1]["end"], "Ending is where summary can either land or flatten.", 7)

        for fence in extract_fences(post):
            context_start = max(post["body_start"], fence["start"] - 2)
            context_end = min(post["body_start"] + len(post["lines"]) - 1, fence["end"] + 2)
            context = "\n".join(post["lines"][context_start - post["body_start"] : context_end - post["body_start"] + 1])
            add_candidate(candidates, post, "demo_usefulness", context, context_start, context_end, "Demo-like artifact should teach faster than prose, not decorate.", 9)

        for section in sections(post):
            words = count_words(section["text"])
            if words > 230:
                excerpt_lines = section["text"].splitlines()
                excerpt = "\n".join(excerpt_lines[:8])
                add_candidate(candidates, post, "over_explanation", excerpt, section["start"], min(section["end"], section["start"] + 7), "Long section may be doing more proof work than the reader needs.", 6)
            if re.search(r"(?i)(want\s*/\s*need\s*/\s*get|pipeline|workflow|gate|stage|framework|principle)", section["text"]) and words > 80:
                excerpt_lines = section["text"].splitlines()
                excerpt = "\n".join(excerpt_lines[:8])
                add_candidate(candidates, post, "scaffold_leakage", excerpt, section["start"], min(section["end"], section["start"] + 7), "Process language can clarify, but it can also expose the scaffolding.", 7)

        for para in paras:
            text = para["text"]
            words = count_words(text)
            if 4 <= words <= 16 and not text.startswith("#") and not text.startswith("```"):
                score = 8 if re.search(r"(?i)\b(not|never|only|should|invisible|magic|boring|truth|receipt|workflow|automation)\b", text) else 5
                add_candidate(candidates, post, "line_to_keep_detection", text, para["start"], para["end"], "Compact line may carry voice and should be protected or deliberately rejected.", score)
            if words >= 25 and not re.search(r"\b(I|me|my|we|us|our|you|your)\b", text, flags=re.IGNORECASE) and re.search(r"(?i)(user|people|system|assistant|agent|workflow)", text):
                add_candidate(candidates, post, "personal_voice_vs_abstraction", text, para["start"], para["end"], "Systems prose may be right, or it may be hiding a stronger speaker/reader relationship.", 6)

    deduped: list[Candidate] = []
    seen: set[tuple[str, str, int]] = set()
    for candidate in sorted(candidates, key=lambda item: item.heuristic_score, reverse=True):
        key = (candidate.post, candidate.category_id, candidate.line_start)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)
    return deduped


def extract_text_from_json(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(text for text in (extract_text_from_json(item) for item in value) if text)
    if isinstance(value, dict):
        outputs = value.get("outputs")
        if isinstance(outputs, list):
            text = "\n".join(extract_text_from_json(item) for item in outputs).strip()
            if text:
                return text
        for key in ("text", "content", "message", "response", "output", "final"):
            if key in value:
                text = extract_text_from_json(value[key])
                if text:
                    return text
        return "\n".join(text for text in (extract_text_from_json(item) for item in value.values()) if text)
    return ""


def parse_json_object(text: str) -> Any:
    try:
        return json.loads(text)
    except Exception:
        pass
    match = re.search(r"```json\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        return json.loads(match.group(1))
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start : end + 1])
    raise ValueError("no JSON object found in model output")


def run_model(prompt: str, args: argparse.Namespace) -> dict[str, Any]:
    models = [args.model] + list(args.fallback_model or [])
    attempts: list[dict[str, Any]] = []
    for model in models:
        command = ["openclaw", "infer", "model", "run", "--gateway", "--json", "--prompt", prompt, "--model", model]
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
            attempts.append({"model": model, "ok": False, "error": f"timeout after {args.timeout}s", "stdout": exc.stdout or ""})
            continue
        raw = proc.stdout or ""
        parsed: Any = None
        text = raw.strip()
        try:
            parsed = json.loads(raw)
            text = extract_text_from_json(parsed).strip()
        except Exception:
            parsed = None
        attempt = {"model": model, "ok": proc.returncode == 0, "returncode": proc.returncode, "stdout": raw[-4000:], "json": parsed, "text": text}
        attempts.append(attempt)
        if proc.returncode == 0:
            return {**attempt, "attempts": attempts}
    last = attempts[-1] if attempts else {"error": "no models configured", "text": ""}
    return {**last, "ok": False, "attempts": attempts}


def build_model_prompt(candidates: list[Candidate], rubric: dict[str, Any], max_items: int) -> str:
    slim_rubric = [
        {
            "id": category["id"],
            "label": category["label"],
            "concern": category["concern"],
            "question": category["question"],
            "options": category["options"],
        }
        for category in rubric["categories"]
    ]
    candidate_payload = [
        {
            "id": candidate.id,
            "post": candidate.post,
            "title": candidate.title,
            "suggested_category": candidate.category_id,
            "excerpt": candidate.excerpt[:1200],
            "reason": candidate.reason,
            "heuristic_score": candidate.heuristic_score,
        }
        for candidate in candidates[:60]
    ]
    return (
        "You are selecting excerpts for a human taste review of blog posts.\n"
        "Pick the highest-signal excerpts where the user's taste answer would improve the writing skill.\n"
        "Avoid duplicates. Prefer excerpts that test different concerns.\n"
        f"Return exactly JSON with an `items` array of at most {max_items} items.\n"
        "Each item must include: candidate_id, category_id, concern, question, options, rank_reason, priority.\n"
        "Use options from the rubric when possible.\n\n"
        f"Rubric:\n{json.dumps(slim_rubric, indent=2)}\n\n"
        f"Candidates:\n{json.dumps(candidate_payload, indent=2)}\n"
    )


def deterministic_selection(candidates: list[Candidate], rubric: dict[str, Any], max_items: int) -> list[dict[str, Any]]:
    categories = {category["id"]: category for category in rubric["categories"]}
    selected: list[dict[str, Any]] = []
    used_categories: set[str] = set()
    for candidate in sorted(candidates, key=lambda item: item.heuristic_score, reverse=True):
        if candidate.category_id in used_categories and len(used_categories) < min(max_items, len(categories)):
            continue
        category = categories[candidate.category_id]
        selected.append(
            {
                "candidate_id": candidate.id,
                "category_id": candidate.category_id,
                "concern": category["concern"],
                "question": category["question"],
                "options": category["options"],
                "rank_reason": candidate.reason,
                "priority": max(1, min(5, candidate.heuristic_score // 2)),
            }
        )
        used_categories.add(candidate.category_id)
        if len(selected) >= max_items:
            return selected
    return selected


def select_review_items(candidates: list[Candidate], rubric: dict[str, Any], args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if args.offline:
        return deterministic_selection(candidates, rubric, args.max_items), {"ok": True, "offline": True}
    model_result = run_model(build_model_prompt(candidates, rubric, args.max_items), args)
    if not model_result.get("ok"):
        return deterministic_selection(candidates, rubric, args.max_items), {"ok": False, "fallback": "deterministic", "model": model_result}
    try:
        parsed = parse_json_object(model_result.get("text", ""))
        items = parsed.get("items", [])
        if not isinstance(items, list):
            raise ValueError("items is not a list")
        return items[: args.max_items], {"ok": True, "offline": False, "model": model_result}
    except Exception as exc:
        return deterministic_selection(candidates, rubric, args.max_items), {"ok": False, "fallback": "deterministic", "error": repr(exc), "model": model_result}


def hydrate_items(items: list[dict[str, Any]], candidates: list[Candidate], rubric: dict[str, Any]) -> list[dict[str, Any]]:
    by_id = {candidate.id: candidate for candidate in candidates}
    categories = {category["id"]: category for category in rubric["categories"]}
    hydrated: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        candidate = by_id.get(str(item.get("candidate_id")))
        if candidate is None:
            continue
        category_id = item.get("category_id") or candidate.category_id
        category = categories.get(category_id) or categories[candidate.category_id]
        hydrated.append(
            {
                "review_id": f"r{index:02d}",
                "candidate": candidate.to_json(),
                "category_id": category["id"],
                "category_label": category["label"],
                "concern": item.get("concern") or category["concern"],
                "question": item.get("question") or category["question"],
                "options": item.get("options") if isinstance(item.get("options"), list) and len(item.get("options")) >= 2 else category["options"],
                "rank_reason": item.get("rank_reason") or candidate.reason,
                "priority": item.get("priority", candidate.heuristic_score),
            }
        )
    return hydrated


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Write Post Taste Review",
        "",
        f"Ran at: {report['ran_at']}",
        f"Posts scanned: {report['posts_scanned']}",
        f"Candidates extracted: {report['candidates_extracted']}",
        f"Review items: {len(report['review_items'])}",
        "",
        "Use this as a short review packet. You do not need to read the full posts.",
        "",
    ]
    for item in report["review_items"]:
        candidate = item["candidate"]
        lines.extend(
            [
                f"## {item['review_id']} · {item['category_label']}",
                "",
                f"Source: `{candidate['post']}` lines {candidate['line_start']}-{candidate['line_end']}",
                "",
                "Excerpt:",
                "",
                "```text",
                candidate["excerpt"].strip(),
                "```",
                "",
                f"Why flagged: {item['rank_reason']}",
                "",
                f"Question: {item['question']}",
                "",
            ]
        )
        for idx, option in enumerate(item["options"], start=1):
            lines.append(f"{idx}. {option}")
        lines.append("")
    return "\n".join(lines)


def update_task_file(report: dict[str, Any]) -> None:
    TASK_FILE.write_text(
        "# Write Post Taste Eval\n\n"
        "Goal: use small human taste checks to improve the writing skill without asking for full-post review.\n\n"
        f"Status: review_ready\n"
        f"Last run: {report['ran_at']}\n"
        f"Posts scanned: {report['posts_scanned']}\n"
        f"Candidates extracted: {report['candidates_extracted']}\n"
        f"Review items: {len(report['review_items'])}\n"
        "Next slice: present the highest-signal review questions to the user, then synthesize taste rules.\n"
        "Blocker: waiting for user taste answers.\n\n"
        "Artifacts:\n"
        "- `evals/write-post-taste-rubric.json`\n"
        "- `scripts/write-post-taste-eval.py`\n"
        "- `logs/write-post-taste/latest.json`\n"
        "- `logs/write-post-taste/latest.md`\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a human taste-review packet for write-post.")
    parser.add_argument("--offline", action="store_true", help="Use deterministic selection instead of model ranking.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Primary model for ranking excerpts.")
    parser.add_argument("--fallback-model", action="append", default=[], help="Fallback model id. May be repeated.")
    parser.add_argument("--timeout", type=int, default=180, help="Model timeout in seconds.")
    parser.add_argument("--max-items", type=int, default=8, help="Maximum review items to select.")
    parser.add_argument("--json", action="store_true", help="Print full JSON report.")
    args = parser.parse_args()

    rubric = load_json(RUBRIC_FILE)
    posts = [parse_post(path) for path in sorted(POST_DIR.glob("*.md"))]
    candidates = extract_candidates(posts)
    selected, selection = select_review_items(candidates, rubric, args)
    review_items = hydrate_items(selected, candidates, rubric)

    report = {
        "ran_at": now_utc(),
        "ok": bool(review_items),
        "posts_scanned": len(posts),
        "candidates_extracted": len(candidates),
        "review_items": review_items,
        "selection": selection,
        "model": None if args.offline else args.model,
    }

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    write_json(LOG_DIR / "latest.json", report)
    (LOG_DIR / "latest.md").write_text(render_markdown(report))
    with (LOG_DIR / "history.jsonl").open("a") as f:
        f.write(json.dumps(report, sort_keys=True) + "\n")
    update_task_file(report)

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        mode = "offline" if args.offline else f"model={args.model}"
        print(
            "write-post-taste: "
            f"{'PASS' if report['ok'] else 'FAIL'} | mode={mode} | "
            f"posts={report['posts_scanned']} | "
            f"candidates={report['candidates_extracted']} | "
            f"review_items={len(report['review_items'])}"
        )
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
