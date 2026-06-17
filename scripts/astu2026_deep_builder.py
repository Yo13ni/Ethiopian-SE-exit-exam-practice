"""Rich deep explanations for ASTU 2026 model exit exam rounds."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from bdu_concept_engine import _glossary_lookup, _stem_intent, explain_correct_option, explain_wrong_option
from unified_deep_formatter import format_entry, is_shallow_body, is_shallow_overview, strip_option_body
from unified_topic_enricher import explain_correct_rich, explain_wrong_rich, is_generic_fallback

ROOT = Path(__file__).resolve().parent.parent


def _norm(text: str) -> str:
    text = re.sub(r"\s+", " ", text.lower())
    text = re.sub(r"[^\w\s/\.]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _opts(q: dict) -> dict[str, str]:
    return {o["key"]: o["text"] for o in q["options"]}


def _study_tip(topic: str, stem: str) -> str:
    tips = {
        "C++": "Trace code on paper; remember #include \"file\" for user headers and arrays decay to pointers.",
        "Fundamentals of Programming": "Stack = scope lifetime; heap = new/delete. Local vars are uninitialized garbage.",
        "Data Structures": "Know FIFO vs LIFO, stable vs unstable sorts, and when to use stack for recursion.",
        "Java / OOP": "Abstract classes may have constructors; interfaces cannot. super() is inserted implicitly.",
        "Web Development": "HTML structure, CSS box model, JS client-side, HTTP stateless + sessions for state.",
        "Android": "Activity = screen; Fragment = reusable portion; Manifest declares app metadata.",
        "Database": "Weak entity = total participation + partial key. ACID: Atomicity, Consistency, Isolation, Durability.",
        "Operating Systems": "fork() creates process; deadlock needs hold-and-wait + circular wait + no preemption + mutual exclusion.",
        "Software Engineering": "Waterfall is sequential; Agile is iterative. RE bridges stakeholders and developers.",
        "Software Architecture": "High cohesion + low coupling. Patterns solve recurring design problems.",
        "Project Management": "Triple constraint: scope, time, cost. Float = slack without delaying project end.",
        "Software Testing": "Unit → Integration → System → Acceptance. Regression after every change.",
        "Software Maintenance": "Corrective fixes faults; perfective improves; adaptive handles environment change.",
        "Networking": "OSI: Physical→Data Link→Network→Transport→Session→Presentation→Application.",
        "Security": "CIA triad. IDS detects; IPS blocks. Hash verifies integrity, not encryption.",
        "AI / ML": "Supervised = labeled data. BFS shallowest first. A* uses f=g+h.",
    }
    if topic in tips:
        return tips[topic]
    if "output" in stem.lower() or "cout" in stem.lower():
        return "Trace code line-by-line; watch scope, references, and operator precedence."
    return f"Review {topic} definitions and redo this question in Review mode."


def _build_overview(q: dict) -> str:
    topic = q.get("topic", "General")
    answer = q["answer"]
    opts = _opts(q)
    correct_text = opts.get(answer, "")
    stem = q.get("text", "").strip()
    intent = _stem_intent(stem)
    gloss = _glossary_lookup(correct_text)

    parts: list[str] = []
    if "output" in stem.lower() or "cout" in stem.lower() or "printf" in stem.lower():
        parts.append(
            "This is a code-tracing question: execute each statement in order, tracking variable values, "
            "scope rules, and side effects before comparing with the options."
        )
    elif intent != "the specific concept tested in this question":
        parts.append(f"This {topic} question tests {intent}.")
    else:
        parts.append(stem[:300] + ("…" if len(stem) > 300 else ""))

    if gloss:
        parts.append(f"Core concept: {gloss}.")
    elif correct_text:
        parts.append(f"The keyed answer is {answer} — {correct_text}.")

    wrong = [k for k in opts if k != answer]
    if wrong and len(stem) < 250:
        parts.append(
            f"Eliminate options that confuse adjacent {topic} terms before confirming {answer}."
        )
    return " ".join(parts)


def _explain_option(q: dict, key: str, text: str) -> str:
    rich = explain_correct_rich(q, text) if key == q["answer"] else explain_wrong_rich(q, key, text)
    if not is_generic_fallback(rich) and not is_shallow_body(rich):
        return rich
    if key == q["answer"]:
        base = explain_correct_option(q, text)
        if base and "correctly answers" not in base:
            return base
    else:
        base = explain_wrong_option(q, key, text)
        if base and "does not answer" not in base:
            return base
    topic = q.get("topic", "General")
    if key == q["answer"]:
        return (
            f'"{text}" is correct because it matches the standard {topic} definition or behavior '
            f"required by this scenario — verify against lecture notes if any detail feels ambiguous."
        )
    return (
        f'"{text}" is incorrect because it describes a different {topic} concept, applies the wrong rule, '
        f"or would produce a different outcome than the keyed answer in this scenario."
    )


def _generate_entry(q: dict) -> dict[str, Any]:
    opts = _opts(q)
    options = {key: _explain_option(q, key, text) for key, text in opts.items()}
    return {
        "overview": _build_overview(q),
        "options": options,
        "studyTip": _study_tip(q.get("topic", "General"), q.get("text", "")),
    }


def _load_external_bank() -> list[tuple[str, dict, dict]]:
    """Index (stem, deep_raw, source_question) from existing exams."""
    index: list[tuple[str, dict, dict]] = []
    catalog_path = ROOT / "data" / "catalog.json"
    if not catalog_path.exists():
        return index

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    skip = {"astu2026r1", "astu2026r2", "astu2026r3", "2017"}

    for exam in catalog.get("exams", []):
        if exam["id"] in skip:
            continue
        q_path = ROOT / exam["questionsPath"]
        d_path = ROOT / exam["deepPath"]
        if not q_path.exists() or not d_path.exists():
            continue
        qs = json.loads(q_path.read_text(encoding="utf-8"))["questions"]
        deep_all = json.loads(d_path.read_text(encoding="utf-8"))
        for q in qs:
            num = str(q.get("examNumber", q.get("id", "")))
            if num not in deep_all:
                continue
            entry = deep_all[num]
            if len(entry.get("overview", "")) < 40:
                continue
            index.append((_norm(q["text"]), entry, q))
    return index


_BANK: list[tuple[str, dict, dict]] | None = None


def _match_external(q: dict) -> dict[str, Any] | None:
    global _BANK
    if _BANK is None:
        _BANK = _load_external_bank()

    best_score = 0.0
    best: tuple[dict, dict] | None = None
    for ref_stem, deep, src_q in _BANK:
        score = _similarity(q["text"], ref_stem)
        if score > best_score:
            best_score = score
            best = (deep, src_q)

    if best_score < 0.88 or not best:
        return None
    deep, src_q = best
    if src_q.get("answer") != q.get("answer"):
        return None

    opts = _opts(q)
    src_opts = {o["key"]: o["text"] for o in src_q["options"]}
    matched = 0
    for key in "ABCD":
        if key in opts and key in src_opts:
            if _similarity(opts[key], src_opts[key]) >= 0.85:
                matched += 1
    if matched < 3:
        return None

    options: dict[str, str] = {}
    for key in opts:
        raw = deep.get("options", {}).get(key, "")
        if isinstance(raw, str) and raw.startswith(("✓", "✗", "Option")):
            body = raw.split(". ", 1)[-1] if ". " in raw else raw
            options[key] = strip_option_body(body, opts[key])
        elif isinstance(raw, str) and len(raw) > 20:
            options[key] = strip_option_body(raw, opts[key])
        else:
            options[key] = _explain_option(q, key, opts[key])

    return {
        "overview": deep.get("overview", _build_overview(q)),
        "options": options,
        "studyTip": deep.get("studyTip") or _study_tip(q.get("topic", ""), q.get("text", "")),
    }


def build_deep_entry(q: dict) -> dict[str, Any]:
    raw = _match_external(q)
    if not raw or is_shallow_overview(raw["overview"]):
        raw = _generate_entry(q)
    return format_entry(raw, q)
