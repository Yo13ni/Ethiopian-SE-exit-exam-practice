"""Format deep explanations in model1 style (✓/✗ options, ✅ answer line)."""

from __future__ import annotations

import re
from typing import Any

OPTION_PREFIX = re.compile(
    r'^Option [A-D] \((?:CORRECT|INCORRECT)\): "(?:[^"\\]|\\.)*"\.\s*',
)

SHALLOW_MARKERS = (
    "is a common distractor",
    "does not satisfy the specific requirement",
    "sounds plausible but is wrong because",
    "does not answer the specific concept",
    "aligns with standard software-engineering curriculum",
    "the specific concept tested in this question",
    "These are different concepts; do not confuse them on the exam",
    "Students often pick this when they recognize a keyword",
    "On exit exams, when an option states the canonical rule",
)

SHALLOW_OVERVIEW_MARKERS = (
    "This ",
    " question evaluates whether you can identify",
    "**Concept (",
    "the specific concept tested in this question",
    "Each option below explains the underlying concept",
)


def strip_option_body(text: str, option_text: str = "") -> str:
    body = text.strip()
    while True:
        m = OPTION_PREFIX.match(body)
        if m:
            body = body[m.end():].strip()
            continue
        if body.startswith("✓ CORRECT."):
            body = body[len("✓ CORRECT."):].strip()
            continue
        if body.startswith("✗ Not the answer."):
            body = body[len("✗ Not the answer."):].strip()
            continue
        break

    if option_text:
        q = re.escape(option_text)
        body = re.sub(rf'^"{q}"\s+sounds plausible but is wrong because\s+', "", body, flags=re.I)
        body = re.sub(rf'^"{q}"\s+is correct because\s+', "", body, flags=re.I)
        body = re.sub(rf'^"{q}"\s+', "", body)

    return body.strip()


def strip_overview(text: str) -> str:
    overview = text.strip()
    overview = re.sub(r"\n\n✅ Exact answer:.*", "", overview, flags=re.DOTALL)
    overview = re.sub(r"\n\n✅ Answer:.*", "", overview, flags=re.DOTALL)
    overview = re.sub(r"\s*Key idea \([^)]+\):[^\n]*", "", overview)
    overview = re.sub(r"\*\*Concept \([^)]+\):\*\*[^*]*", "", overview)
    overview = re.sub(r"\*\*Correct answer: [A-D]\*\*[^.]*\.?\s*", "", overview)
    overview = re.sub(r"Each option below explains the underlying concept and why it fits or fails\.?\s*", "", overview)
    overview = re.sub(r"Read every option literally; exit exams often trap you with partially true statements.*", "", overview)
    return re.sub(r"\n{3,}", "\n\n", overview).strip()


def is_shallow_body(body: str) -> bool:
    b = body.strip()
    if any(m in b for m in SHALLOW_MARKERS):
        return True
    if len(b) < 18:
        return True
    if len(b) < 45 and b.count(" ") < 4:
        return True
    return False


def is_shallow_overview(overview: str) -> bool:
    o = overview.strip()
    if len(o) < 60:
        return True
    if "**Concept (" in o and "the specific concept tested" in o:
        return True
    if " question evaluates whether you can identify" in o:
        return True
    return False


def format_overview(overview: str, q: dict) -> str:
    clean = strip_overview(overview)
    ans = q["answer"]
    correct_text = next(o["text"] for o in q["options"] if o["key"] == ans)
    return f"{clean}\n\n✅ Answer: {ans} — {correct_text}"


def format_option_body(body: str, key: str, q: dict) -> str:
    if key == q["answer"]:
        return f"✓ CORRECT. {body}"
    return f"✗ Not the answer. {body}"


def strip_entry(entry: dict[str, Any], q: dict) -> dict[str, Any]:
    opts = {o["key"]: o["text"] for o in q["options"]}
    return {
        "overview": strip_overview(entry.get("overview", "")),
        "options": {
            k: strip_option_body(v, opts.get(k, ""))
            for k, v in entry.get("options", {}).items()
        },
        "studyTip": entry.get("studyTip", "").strip(),
    }


def format_entry(raw: dict[str, Any], q: dict) -> dict[str, Any]:
    return {
        "overview": format_overview(raw["overview"], q),
        "options": {
            k: format_option_body(raw["options"][k], k, q)
            for k in raw["options"]
            if k in {o["key"] for o in q["options"]}
        },
        "studyTip": raw.get("studyTip", ""),
        "source": "offline-deep",
    }
