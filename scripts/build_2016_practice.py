"""Build 2016 Software Engineering Exit Exam for the practice app."""

from __future__ import annotations

import json
import re
from pathlib import Path

from exam2016_data import EXTRA_QUESTIONS, FOCUS_GUIDE, QUESTION_FIXES

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / "exam-app" / "data" / "exam.json"
OUT = ROOT / "data" / "exams" / "2016" / "questions.json"

BAD_MARKERS = (
    "ocr",
    "manual review",
    "unavailable",
    "see question",
    "review the original",
    "try eliminating",
    "flag this question",
)


def is_bad_question(q: dict) -> bool:
    blob = q.get("text", "") + " " + " ".join(o.get("text", "") for o in q.get("options", []))
    low = blob.lower()
    return any(m in low for m in BAD_MARKERS) or len(q.get("text", "")) < 15


def normalize_topic(topic: str) -> str:
    if topic in ("AI / ML", "AI / ML / Data Mining"):
        return "AI / ML"
    if topic == "General":
        return "Software Engineering"
    return topic


def concept_line(topic: str, answer: str, options: list[dict]) -> str:
    correct = next((o for o in options if o["key"] == answer), None)
    if correct:
        t = correct["text"]
        return f"Key idea ({topic}): {t[:120]}{'…' if len(t) > 120 else ''}"
    return f"Key idea ({topic}): answer {answer}"


def to_practice_question(num: int, text: str, options: list[dict], answer: str, topic: str) -> dict:
    topic = normalize_topic(topic)
    return {
        "examNumber": num,
        "id": num,
        "topic": topic,
        "text": text.strip(),
        "options": options,
        "answer": answer,
        "concept": concept_line(topic, answer, options),
    }


def apply_source_question(num: int, q: dict) -> dict:
    qid = q["id"]
    if qid in QUESTION_FIXES:
        fix = QUESTION_FIXES[qid]
        return to_practice_question(num, fix["text"], fix["options"], fix["answer"], fix["topic"])

    if is_bad_question(q):
        raise ValueError(f"Question id {qid} still has bad OCR and no fix in QUESTION_FIXES")

    options = [{"key": o["key"], "text": o["text"].strip()} for o in q["options"]]
    return to_practice_question(num, q["text"], options, q["answer"], q.get("topic", "General"))


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    source = sorted(data["questions"], key=lambda q: q["id"])
    questions = [apply_source_question(i, q) for i, q in enumerate(source, start=1)]

    start = len(questions) + 1
    for i, item in enumerate(EXTRA_QUESTIONS, start=start):
        text, opts, answer, topic = item
        options = [{"key": k, "text": t} for k, t in opts]
        questions.append(to_practice_question(i, text, options, answer, topic))

    payload = {
        "title": "2016 Software Engineering Exit Exam",
        "source": "2016-exitexam.pdf — Ethiopian national university exit exam (Software Engineering)",
        "total": len(questions),
        "timeLimitHours": 3,
        "dataRevision": 1,
        "focusGuide": FOCUS_GUIDE,
        "questions": questions,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(questions)} questions -> {OUT}")


if __name__ == "__main__":
    main()
