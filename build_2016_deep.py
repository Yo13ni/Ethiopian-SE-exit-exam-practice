"""Build deep explanations for 2016 Exit Exam."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from generic_deep_builder import build_deep_entry, enrich_with_concept

ROOT = Path(__file__).parent
QUESTIONS_PATH = ROOT / "data" / "exams" / "2016" / "questions.json"
OUT_PATH = ROOT / "data" / "exams" / "2016" / "deep_explanations.json"
DEEP_2015_PATH = ROOT / "data" / "exams" / "2015" / "deep_explanations.json"
QUESTIONS_2015_PATH = ROOT / "data" / "exams" / "2015" / "questions.json"


def _norm(text: str) -> str:
    text = re.sub(r"\s+", " ", text.lower())
    text = re.sub(r"[^\w\s/\.]", " ", text)
    return re.sub(r"\s+", " ", text).strip()[:160]


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def load_2015_index() -> list[tuple[str, dict, dict]]:
    if not QUESTIONS_2015_PATH.exists() or not DEEP_2015_PATH.exists():
        return []
    qs = json.loads(QUESTIONS_2015_PATH.read_text(encoding="utf-8"))["questions"]
    deep = json.loads(DEEP_2015_PATH.read_text(encoding="utf-8"))
    out: list[tuple[str, dict, dict]] = []
    for q in qs:
        num = str(q.get("examNumber", q.get("id", "")))
        if num in deep:
            out.append((_norm(q["text"]), deep[num], q))
    return out


def find_2015_match(stem: str, index: list[tuple[str, dict, dict]], threshold: float = 0.72) -> tuple[dict, dict] | None:
    best_score = 0.0
    best: tuple[dict, dict] | None = None
    for ref_stem, deep_entry, q2015 in index:
        score = _similarity(stem, ref_stem)
        if score > best_score:
            best_score = score
            best = (deep_entry, q2015)
    if best_score >= threshold and best:
        return best
    return None


def _extract_body(option_line: str) -> str:
    if ". " in option_line:
        return option_line.split(". ", 1)[-1]
    return option_line


def merge_curated_overview(entry: dict, curated: dict) -> dict:
    """Keep 2016-accurate option tags; borrow rich overview/tip from 2015 when stems match."""
    entry["overview"] = curated.get("overview", entry["overview"])
    tip = curated.get("studyTip", "")
    if tip and tip not in entry.get("studyTip", ""):
        entry["studyTip"] = tip
    return entry


def match_option_bodies(q: dict, curated: dict, q2015: dict) -> dict[str, str] | None:
    """Map 2015 option teaching text onto 2016 keys by option-text similarity."""
    bodies: dict[str, str] = {}
    curated_opts = curated.get("options", {})
    keys_2015 = {o["key"]: o["text"] for o in q2015["options"]}
    keys_2016 = {o["key"]: o["text"] for o in q["options"]}
    used: set[str] = set()

    for key6, text6 in keys_2016.items():
        best_key5 = None
        best_score = 0.0
        for key5, text5 in keys_2015.items():
            if key5 in used:
                continue
            score = _similarity(text6, text5)
            if score > best_score:
                best_score = score
                best_key5 = key5
        if best_key5 and best_score >= 0.55:
            used.add(best_key5)
            bodies[key6] = _extract_body(curated_opts.get(best_key5, ""))
    return bodies if len(bodies) >= 3 else None


def build_entry(q: dict, index: list[tuple[str, dict, dict]]) -> dict[str, Any]:
    correct = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}
    entry = build_deep_entry(q)

    matched = find_2015_match(q["text"], index)
    if matched:
        curated, q2015 = matched
        entry = merge_curated_overview(entry, curated)
        bodies = match_option_bodies(q, curated, q2015)
        if bodies:
            for key in "ABCD":
                text = opts.get(key, "")
                tag = "CORRECT" if key == correct else "INCORRECT"
                body = bodies.get(key, _extract_body(entry["options"][key]))
                entry["options"][key] = f'Option {key} ({tag}): "{text}". {body}'
        entry["source"] = "2015-enriched"
    else:
        entry = enrich_with_concept(q, entry)
        entry["source"] = "generated"

    return entry


def main() -> None:
    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    index = load_2015_index()
    out: dict[str, dict] = {}
    stats: dict[str, int] = {"2015-enriched": 0, "generated": 0}

    for q in data["questions"]:
        num = str(q["examNumber"])
        entry = build_entry(q, index)
        src = entry.pop("source", "generated")
        stats[src if src in stats else "generated"] += 1
        out[num] = entry

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(out)} deep explanations -> {OUT_PATH}")
    print("Sources:", stats)


if __name__ == "__main__":
    main()
