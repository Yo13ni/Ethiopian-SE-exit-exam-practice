"""Build 2025 MoEE Exit Exam questions.json."""

from __future__ import annotations

import json
from pathlib import Path

from moe2025_exam_data import FOCUS_GUIDE, RAW

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "data" / "exams" / "moe2025" / "questions.json"


def concept_line(topic: str, answer: str, options: list[dict]) -> str:
    correct = next((o for o in options if o["key"] == answer), None)
    if correct:
        t = correct["text"]
        return f"Key idea ({topic}): {t[:120]}{'…' if len(t) > 120 else ''}"
    return f"Key idea ({topic}): answer {answer}"


def main() -> None:
    questions = []
    for i, (text, opts, answer, topic) in enumerate(RAW, start=1):
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

    payload = {
        "title": "2025 MoEE Software Engineering Exit Exam",
        "source": "2025 Ethiopian University Exit Exam for Software Engineering (MoEE blueprint)",
        "total": len(questions),
        "focusGuide": FOCUS_GUIDE,
        "questions": questions,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(questions)} questions -> {OUT_PATH}")


if __name__ == "__main__":
    main()
