"""Build ASTU Software Engineering exam questions.json from PDF text."""

from __future__ import annotations

import json
import re
from pathlib import Path

from astu_answers import ANSWERS
from astu_exam_data import FOCUS_GUIDE, MANUAL_OVERRIDES
from astu_parser import parse_all_questions

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "exams" / "astu" / "raw_text.json"
OUT_PATH = ROOT / "data" / "exams" / "astu" / "questions.json"

TOPIC_RULES: list[tuple[str, str]] = [
    ("Project Management", r"COCOMO|effort cost|estimation|project metric|project indicator|decomposition|Parkinson|algorithmic cost|risk projection|technical risk|business risk"),
    ("Software Testing", r"black box|maintenance test|quality model|ISO9126|Mc Call|defect|DRE|conformance"),
    ("Software Architecture", r"RUP|behavioral model|context model|spiral model|reengineering|reverse engineering|forward engineering|model-driven"),
    ("Software Engineering", r"SDLC|waterfall|RAD|prototyp|spiral|agile|incremental|4GT|software product|software maintenance|generic process|ASD|plan-driven|evolutionary"),
    ("General", r"DFD|structured analysis|data flow|data store|aviation|RTCADO|certification|algorithm|software design"),
]


def classify(text: str) -> str:
    for topic, pat in TOPIC_RULES:
        if re.search(pat, text, re.I):
            return topic
    return "Software Engineering"


def concept_line(topic: str, answer: str, options: list[dict]) -> str:
    correct = next((o for o in options if o["key"] == answer), None)
    if correct:
        return f"Key idea ({topic}): {correct['text']}"
    return f"Key idea ({topic}): answer {answer}"


def load_full_text() -> str:
    pages = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    return "\n".join(p["text"] for p in pages)


def build_questions() -> tuple[list[dict], list[str]]:
    parsed = parse_all_questions(load_full_text())
    questions: list[dict] = []
    skipped: list[str] = []

    for item in parsed:
        exam_num = item["examNumber"]
        override = MANUAL_OVERRIDES.get(exam_num, {})
        text = override.get("text") or item["text"]
        options = override.get("options") or item["options"]
        answer = override.get("answer") or ANSWERS.get(exam_num)

        if not answer:
            skipped.append(f"Q{exam_num}: missing answer key")
            continue
        if len(options) < 2:
            skipped.append(f"Q{exam_num}: fewer than 2 options")
            continue

        topic = override.get("topic") or classify(text + " " + " ".join(o["text"] for o in options))
        questions.append({
            "examNumber": exam_num,
            "id": len(questions) + 1,
            "topic": topic,
            "text": text,
            "options": options,
            "answer": answer,
            "concept": concept_line(topic, answer, options),
        })

    found = {q["examNumber"] for q in questions}
    for n in range(1, 61):
        if n not in found:
            skipped.append(f"Q{n}: not parsed from PDF")

    return questions, skipped


def main() -> None:
    if not RAW_PATH.exists():
        print(f"Missing {RAW_PATH}. Run extract_astu_pdf.py first.")
        return
    questions, skipped = build_questions()
    payload = {
        "title": "ASTU Software Engineering MCQs",
        "source": "ASTU Software Eng.pdf — Software Engineering MCQ bank",
        "total": len(questions),
        "focusGuide": FOCUS_GUIDE,
        "questions": questions,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(questions)} questions -> {OUT_PATH}")
    if skipped:
        print(f"Skipped / missing ({len(skipped)}):")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
