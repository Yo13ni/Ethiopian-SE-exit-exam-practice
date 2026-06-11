"""Build 2016 exam from OCR-ordered official bank (97 questions)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from exam2016_data import FOCUS_GUIDE
from exam2016_official import OFFICIAL_COUNT, get_official_questions

OUT = ROOT / "data" / "exams" / "2016" / "questions.json"


def concept_line(topic: str, answer: str, options: list[dict]) -> str:
    correct = next((o for o in options if o["key"] == answer), None)
    if correct:
        t = correct["text"]
        return f"Key idea ({topic}): {t[:120]}{'…' if len(t) > 120 else ''}"
    return f"Key idea ({topic}): answer {answer}"


def main() -> None:
    official = get_official_questions()
    questions = []
    for q in official:
        num = q["id"]
        topic = q["topic"]
        options = [{"key": o["key"], "text": o["text"].strip()} for o in q["options"]]
        questions.append(
            {
                "examNumber": num,
                "id": num,
                "topic": topic,
                "text": q["text"].strip(),
                "options": options,
                "answer": q["answer"].upper(),
                "concept": concept_line(topic, q["answer"], options),
            }
        )

    payload = {
        "title": "2016 Software Engineering Exit Exam",
        "source": "2016-exitexam.pdf — Ethiopian national university exit exam (Software Engineering)",
        "total": len(questions),
        "timeLimitHours": 3,
        "dataRevision": 3,
        "focusGuide": FOCUS_GUIDE,
        "questions": questions,
    }

    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(questions)} questions (official OCR order) -> {OUT}")


if __name__ == "__main__":
    main()
