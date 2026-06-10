"""Build deep explanations: BDU concept depth + model1 presentation."""

from __future__ import annotations

import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from bdu_concept_engine import _glossary_lookup, _stem_intent  # noqa: E402
from unified_deep_formatter import (  # noqa: E402
    format_entry,
    is_shallow_body,
    is_shallow_overview,
    strip_entry,
    strip_option_body,
    strip_overview,
)
from unified_topic_enricher import (  # noqa: E402
    explain_correct_rich,
    explain_wrong_rich,
    is_generic_fallback,
)

TOPIC_TIPS: dict[str, str] = {
    "Data Structures": "Write the algorithm on paper and count dominant terms or trace one small example.",
    "Java / OOP": "Trace code on paper. Interfaces cannot be instantiated; constructors match class name and types.",
    "Database": "Normalize step-by-step, check keys and FDs, and verify SQL syntax against schema.",
    "Networking": "Map the scenario to OSI/TCP layers, protocol behavior, or topology properties.",
    "Security": "Use Saltzer-Schroeder principles and CIA triad vocabulary to eliminate distractors.",
    "Software Architecture": "Think quality attributes and ATAM scenarios — not team size or log files.",
    "Software Testing": "Match the question to test levels, coverage types, or traceability definitions.",
    "Project Management": "Identify lifecycle model, risk strategy, or WBS/critical-path terminology.",
    "AI / ML": "Classify learning type or search strategy (informed vs uninformed, optimal vs greedy).",
    "Operating Systems": "Relate to process states, scheduling, memory policies, or deadlock conditions.",
    "Web Development": "Check HTTP methods, CSS selectors, DOM APIs, and client-server roles.",
    "Android": "Activity/Intent/Service/Manifest rules are high-frequency on Ethiopian exit exams.",
    "C++": "Trace small code fragments and validate syntax against C++ compilation rules.",
    "Software Engineering": "SRS, requirements, maintenance types, and SDLC phases — match exact definitions.",
    "General": "DFD symbols, structured analysis steps, and certification standards (DO-178B, UL 1998).",
}


def _norm(text: str) -> str:
    text = re.sub(r"\s+", " ", text.lower())
    text = re.sub(r"[^\w\s/\.]", " ", text)
    return re.sub(r"\s+", " ", text).strip()[:160]


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def build_clean_overview(q: dict) -> str:
    topic = q.get("topic", "General")
    answer = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}
    correct_text = opts.get(answer, "")
    intent = _stem_intent(q.get("text", ""))
    c_def = _glossary_lookup(correct_text)

    stem = q.get("text", "").strip()
    if intent == "the specific concept tested in this question":
        parts = [stem[:280] + ("…" if len(stem) > 280 else "")]
        if c_def:
            parts.append(f"The answer hinges on: {c_def}")
        wrong_keys = [k for k in opts if k != answer]
        if wrong_keys and len(stem) < 200:
            parts.append(
                f"Eliminate distractors that confuse related {topic} terms before picking {answer}."
            )
    else:
        parts = [f"This {topic} question tests {intent}."]
        if c_def:
            parts.append(f"Key concept: {c_def}.")
        elif correct_text:
            parts.append(f"The correct choice is {answer} — {correct_text}.")

    return " ".join(parts)


def _study_tip(q: dict, existing: str = "") -> str:
    if existing and len(existing) > 12 and "Flag this question if the wording was OCR" not in existing:
        return existing
    return TOPIC_TIPS.get(q.get("topic", ""), f"Review {q.get('topic', 'General')} notes and redo this question in Review mode.")


def _raw_bodies_from_engine(q: dict) -> dict[str, Any]:
    correct = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}
    options: dict[str, str] = {}
    for key in "ABCD":
        if key not in opts:
            continue
        text = opts[key]
        if key == correct:
            options[key] = explain_correct_rich(q, text)
        else:
            options[key] = explain_wrong_rich(q, key, text)

    return {
        "overview": build_clean_overview(q),
        "options": options,
        "studyTip": _study_tip(q),
    }


def _upgrade_shallow_raw(raw: dict[str, Any], q: dict, *, curated: bool = False) -> dict[str, Any]:
    if is_shallow_overview(raw["overview"]):
        raw["overview"] = build_clean_overview(q)

    for key in list(raw["options"]):
        body = raw["options"][key]
        needs_upgrade = is_generic_fallback(body) or is_shallow_body(body)
        if not needs_upgrade:
            continue
        text = next((o["text"] for o in q["options"] if o["key"] == key), "")
        if key == q["answer"]:
            raw["options"][key] = explain_correct_rich(q, text)
        else:
            raw["options"][key] = explain_wrong_rich(q, key, text)

    raw["studyTip"] = _study_tip(q, raw.get("studyTip", ""))
    raw.pop("_curated", None)
    return raw


def _raw_from_builder_entry(entry: dict[str, Any], q: dict) -> dict[str, Any]:
    return strip_entry(entry, q)


def _raw_from_2015(q: dict) -> dict[str, Any]:
    from build_curated_deep import CURATED, _build_curated_bank

    if not CURATED:
        _build_curated_bank()
    num = str(q["examNumber"])
    if num not in CURATED:
        return _raw_bodies_from_engine(q)
    base = CURATED[num]
    return {
        "overview": base["overview"],
        "options": dict(base["options"]),
        "studyTip": base["studyTip"],
        "_curated": True,
    }


def _load_2015_index() -> list[tuple[str, dict, dict]]:
    q_path = ROOT / "data" / "exams" / "2015" / "questions.json"
    d_path = ROOT / "data" / "exams" / "2015" / "deep_explanations.json"
    if not q_path.exists() or not d_path.exists():
        return []
    from build_curated_deep import CURATED, _build_curated_bank

    if not CURATED:
        _build_curated_bank()
    qs = json.loads(q_path.read_text(encoding="utf-8"))["questions"]
    out: list[tuple[str, dict, dict]] = []
    for item in qs:
        num = str(item.get("examNumber", item.get("id", "")))
        if num in CURATED:
            out.append((_norm(item["text"]), CURATED[num], item))
    return out


def _extract_body(option_line: str) -> str:
    if ". " in option_line:
        return option_line.split(". ", 1)[-1]
    return option_line


def _match_option_bodies(q: dict, curated: dict, q_source: dict) -> dict[str, str] | None:
    bodies: dict[str, str] = {}
    curated_opts = curated.get("options", {})
    keys_src = {o["key"]: o["text"] for o in q_source["options"]}
    keys_tgt = {o["key"]: o["text"] for o in q["options"]}
    used: set[str] = set()

    for key_tgt, text_tgt in keys_tgt.items():
        best_key_src = None
        best_score = 0.0
        for key_src, text_src in keys_src.items():
            if key_src in used:
                continue
            score = _similarity(text_tgt, text_src)
            if score > best_score:
                best_score = score
                best_key_src = key_src
        if best_key_src and best_score >= 0.55:
            used.add(best_key_src)
            raw_body = curated_opts.get(best_key_src, "")
            if isinstance(raw_body, str):
                bodies[key_tgt] = strip_option_body(_extract_body(raw_body), text_tgt)
    return bodies if len(bodies) >= 3 else None


_CROSS_INDEX: list[tuple[str, dict, dict]] | None = None


def _load_cross_exam_index() -> list[tuple[str, dict, dict]]:
    global _CROSS_INDEX
    if _CROSS_INDEX is not None:
        return _CROSS_INDEX

    index: list[tuple[str, dict, dict]] = []

    from moe2025_deep_builder import BANK, _build_bank

    _build_bank()
    moe_path = ROOT / "data" / "exams" / "moe2025" / "questions.json"
    if moe_path.exists():
        moe_qs = json.loads(moe_path.read_text(encoding="utf-8"))["questions"]
        moe_by_num = {q["examNumber"]: q for q in moe_qs}
        for num, deep in BANK.items():
            if num in moe_by_num:
                index.append((_norm(moe_by_num[num]["text"]), deep, moe_by_num[num]))

    from build_curated_deep import CURATED, _build_curated_bank

    if not CURATED:
        _build_curated_bank()
    q2015_path = ROOT / "data" / "exams" / "2015" / "questions.json"
    if q2015_path.exists():
        qs2015 = json.loads(q2015_path.read_text(encoding="utf-8"))["questions"]
        by_num = {q["examNumber"]: q for q in qs2015}
        for num, deep in CURATED.items():
            n = int(num)
            if n in by_num:
                index.append((_norm(by_num[n]["text"]), deep, by_num[n]))

    from bdu_deep_builder import CURATED as BDU_CURATED

    bdu_q_path = ROOT / "data" / "exams" / "bdu" / "questions.json"
    if bdu_q_path.exists():
        bdu_qs = json.loads(bdu_q_path.read_text(encoding="utf-8"))["questions"]
        bdu_by_num = {q["examNumber"]: q for q in bdu_qs}
        for num, deep in BDU_CURATED.items():
            if num in bdu_by_num:
                index.append((_norm(bdu_by_num[num]["text"]), deep, bdu_by_num[num]))

    catalog_path = ROOT / "data" / "catalog.json"
    if catalog_path.exists():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        for exam in catalog.get("exams", []):
            if exam["id"] in ("2017",):
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
                raw = strip_entry(deep_all[num], q)
                if len(raw.get("overview", "")) > 40:
                    index.append((_norm(q["text"]), raw, q))

    _CROSS_INDEX = index
    return index


def _raw_from_cross_match(q: dict, threshold: float = 0.62) -> dict[str, Any] | None:
    index = _load_cross_exam_index()
    opts = {o["key"]: o["text"] for o in q["options"]}

    best_score = 0.0
    best: tuple[dict, dict] | None = None
    for ref_stem, deep, src_q in index:
        score = _similarity(q["text"], ref_stem)
        if score > best_score:
            best_score = score
            best = (deep, src_q)

    if best_score < threshold or not best:
        return None

    deep, src_q = best
    if best_score < 0.80:
        if src_q.get("topic") != q.get("topic"):
            return None
        if src_q.get("answer") != q.get("answer"):
            return None
    options = dict(deep.get("options", {}))
    bodies = _match_option_bodies(q, deep, src_q)
    if bodies:
        for key in "ABCD":
            if key in bodies:
                options[key] = bodies[key]
            elif key in options:
                options[key] = strip_option_body(str(options[key]), opts.get(key, ""))

    return {
        "overview": deep["overview"],
        "options": options,
        "studyTip": deep.get("studyTip", ""),
        "_curated": True,
    }


def _raw_from_2017(q: dict) -> dict[str, Any]:
    raw = _raw_from_cross_match(q, threshold=0.62)
    if raw:
        return _upgrade_shallow_raw(raw, q, curated=True)
    engine = _raw_bodies_from_engine(q)
    return _upgrade_shallow_raw(engine, q, curated=False)


def _raw_from_2016(q: dict) -> dict[str, Any]:
    index = _load_2015_index()
    correct = q["answer"]
    opts = {o["key"]: o["text"] for o in q["options"]}

    best_score = 0.0
    best: tuple[dict, dict] | None = None
    for ref_stem, deep_entry, q2015 in index:
        score = _similarity(q["text"], ref_stem)
        if score > best_score:
            best_score = score
            best = (deep_entry, q2015)

    if best_score >= 0.72 and best:
        curated, q2015 = best
        options = dict(curated["options"])
        bodies = _match_option_bodies(q, curated, q2015)
        if bodies:
            for key in "ABCD":
                if key in bodies:
                    options[key] = bodies[key]
                elif key in options:
                    options[key] = strip_option_body(str(options[key]), opts.get(key, ""))
        raw = {
            "overview": curated["overview"],
            "options": options,
            "studyTip": curated.get("studyTip", ""),
            "_curated": True,
        }
        return _upgrade_shallow_raw(raw, q, curated=True)

    return _raw_bodies_from_engine(q)


def _raw_from_aau(q: dict) -> dict[str, Any]:
    from aau_deep_builder import BANK, _build_bank

    if not BANK:
        _build_bank()
    num = q["examNumber"]
    if num not in BANK:
        return _raw_bodies_from_engine(q)
    base = BANK[num]
    return {
        "overview": base["overview"],
        "options": dict(base["options"]),
        "studyTip": base["studyTip"],
        "_curated": True,
    }


def _raw_from_bdu(q: dict) -> dict[str, Any]:
    from bdu_deep_builder import CURATED

    num = q.get("examNumber")
    if num in CURATED:
        base = CURATED[num]
        return {
            "overview": base["overview"],
            "options": dict(base["options"]),
            "studyTip": base["studyTip"],
            "_curated": True,
        }
    return _raw_bodies_from_engine(q)


def _raw_from_astu(q: dict) -> dict[str, Any]:
    from astu_deep_builder import build_deep_entry

    entry = build_deep_entry(q)
    raw = _raw_from_builder_entry(entry, q)
    return _upgrade_shallow_raw(raw, q)


def _raw_from_model1(q: dict) -> dict[str, Any]:
    from model1_deep_builder import build_deep_entry

    entry = build_deep_entry(q)
    raw = _raw_from_builder_entry(entry, q)
    raw["_curated"] = True
    return raw


def _raw_from_moe2025(q: dict) -> dict[str, Any]:
    from moe2025_deep_builder import BANK, _build_bank, build_deep_entry

    if not BANK:
        _build_bank()
    entry = build_deep_entry(q)
    raw = _raw_from_builder_entry(entry, q)
    if q["examNumber"] in BANK:
        raw["_curated"] = True
    return raw


RAW_BUILDERS = {
    "2015": _raw_from_2015,
    "2016": _raw_from_2016,
    "2017": _raw_from_2017,
    "aau": _raw_from_aau,
    "bdu": _raw_from_bdu,
    "astu": _raw_from_astu,
    "model1": _raw_from_model1,
    "moe2025": _raw_from_moe2025,
}


def build_deep_entry(q: dict, exam_id: str) -> dict[str, Any]:
    builder = RAW_BUILDERS.get(exam_id, _raw_bodies_from_engine)
    raw = builder(q)
    curated = bool(raw.get("_curated", False))
    raw = _upgrade_shallow_raw(raw, q, curated=curated)
    return format_entry(raw, q)
