"""Rich tutor-style explanations for MoEE Model Exam 1."""

from __future__ import annotations

import re
from typing import Any

from model1_lessons_bulk import OPTION_NOTES as BULK_OPTIONS
from model1_lessons_bulk import OVERVIEWS as BULK_OVERVIEWS
from model1_tutor_engine import BANK as Q1_10_BANK


def _answer_line(q: dict) -> str:
    ans = q["answer"]
    text = next(o["text"] for o in q["options"] if o["key"] == ans)
    return f"\n\n✅ Exact answer: {ans} — {text}"


def _overview(q: dict) -> str:
    n = q["examNumber"]
    if n in Q1_10_BANK:
        return Q1_10_BANK[n]["overview"]
    if n in BULK_OVERVIEWS:
        return BULK_OVERVIEWS[n] + _answer_line(q)
    ans = q["answer"]
    correct = next(o["text"] for o in q["options"] if o["key"] == ans)
    return f"{q.get('text', '')}\n\n✅ Exact answer: {ans} — {correct}"


def _option_body(q: dict, key: str) -> str:
    n = q["examNumber"]
    body = ""
    if n in Q1_10_BANK and key in Q1_10_BANK[n]["options"]:
        body = Q1_10_BANK[n]["options"][key]
    elif n in BULK_OPTIONS and key in BULK_OPTIONS[n]:
        return BULK_OPTIONS[n][key]

    if not body:
        text = next(o["text"] for o in q["options"] if o["key"] == key)
        if key == q["answer"]:
            return f"✓ CORRECT. {text}"
        return f"✗ Not the answer. {text}"

    body = re.sub(r"^(Correct\.|Incorrect\.)\s*", "", body.strip())
    if key == q["answer"]:
        return f"✓ CORRECT. {body}"
    return f"✗ Not the answer. {body}"


def build_deep_entry(q: dict) -> dict[str, Any]:
    n = q["examNumber"]
    tips = Q1_10_BANK.get(n, {}).get("studyTip", "")
    if not tips:
        tips = {
            "Operating Systems": "Scheduling: Long=admit, Medium=swap, Short=CPU. Boot: BIOS → bootloader → kernel.",
            "Java / OOP": "Trace code on paper. Abstract methods must match signature exactly.",
            "Networking": "Map each scenario to an OSI layer before choosing.",
            "Database": "PK = unique + NOT NULL. ON UPDATE CASCADE propagates PK changes to FKs.",
            "Software Testing": "Unit → Integration → System. Decision coverage = every branch T and F.",
            "Web Development": "HTML=structure, CSS=presentation, JS=behavior.",
            "Android": "Lifecycle: onCreate first. APK = Android Package Kit.",
            "AI / ML": "Agent + Environment. Ensemble ≠ Lasso. Overfitting = memorizes training data.",
            "Security": "CIA: Confidentiality, Integrity, Availability.",
            "Project Management": "Validation=right product. Verification=built correctly.",
        }.get(q.get("topic", ""), "Review core definitions and redo this question in Review mode.")

    return {
        "overview": _overview(q),
        "options": {k: _option_body(q, k) for k in "ABCD" if k in {o["key"] for o in q["options"]}},
        "studyTip": tips,
    }


def enrich_with_concept(q: dict, entry: dict) -> dict:
    entry["source"] = "offline-deep"
    return entry
