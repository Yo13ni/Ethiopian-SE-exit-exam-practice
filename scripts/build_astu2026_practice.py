"""Build ASTU 2026 Model Exit Exam rounds (1st, 2nd, 3rd) questions.json."""

from __future__ import annotations

import json
from pathlib import Path

from astu2026r1_data import FOCUS_GUIDE as FOCUS_R1, RAW as RAW_R1
from astu2026r2_data import FOCUS_GUIDE as FOCUS_R2, RAW as RAW_R2
from astu2026r3_data import FOCUS_GUIDE as FOCUS_R3, RAW as RAW_R3

ROOT = Path(__file__).resolve().parent.parent

EXAMS = [
    {
        "id": "astu2026r1",
        "title": "ASTU 1st Round Model Exit Exam",
        "source": "ASTU Software Engineering — 1st Round Model Exit Examination (2hr, 100 MCQs)",
        "raw": RAW_R1,
        "focus": FOCUS_R1,
    },
    {
        "id": "astu2026r2",
        "title": "ASTU 2nd Round Model Exit Exam",
        "source": "ASTU Software Engineering — 2nd Round Model Exit Examination (2hr, 100 MCQs)",
        "raw": RAW_R2,
        "focus": FOCUS_R2,
    },
    {
        "id": "astu2026r3",
        "title": "ASTU 3rd Round Model Exit Exam 2026",
        "source": "ASTU Software Engineering — 3rd Round Model Exit Examination 2026 (2hr, 100 MCQs)",
        "raw": RAW_R3,
        "focus": FOCUS_R3,
    },
]


def concept_line(topic: str, answer: str, options: list[dict]) -> str:
    correct = next((o for o in options if o["key"] == answer), None)
    if correct:
        t = correct["text"]
        return f"Key idea ({topic}): {t[:120]}{'…' if len(t) > 120 else ''}"
    return f"Key idea ({topic}): answer {answer}"


def build_questions(raw: list[tuple]) -> list[dict]:
    questions = []
    for i, (text, opts, answer, topic) in enumerate(raw, start=1):
        options = [{"key": k, "text": t} for k, t in opts]
        questions.append({
            "examNumber": i,
            "id": i,
            "topic": topic,
            "text": text,
            "options": options,
            "answer": answer,
            "concept": concept_line(topic, answer, options),
        })
    return questions


def main() -> None:
    for exam in EXAMS:
        questions = build_questions(exam["raw"])
        out_path = ROOT / "data" / "exams" / exam["id"] / "questions.json"
        payload = {
            "title": exam["title"],
            "source": exam["source"],
            "total": len(questions),
            "focusGuide": exam["focus"],
            "questions": questions,
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote {len(questions)} questions -> {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
