"""Build MoEE Model Exam 1 questions.json from PDF text."""

from __future__ import annotations

import json
import re
from pathlib import Path

from model1_answers import ANSWERS
from model1_exam_data import FOCUS_GUIDE, MANUAL_OVERRIDES
from model1_parser import parse_all_questions

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "exams" / "model1" / "raw_text.json"
OUT_PATH = ROOT / "data" / "exams" / "model1" / "questions.json"

TOPIC_RULES: list[tuple[str, str]] = [
    ("Operating Systems", r"scheduling|bootstrap|bootloader|kernel|procfs|sysfs|loader|linker|compiler|multiprogramming|grouping|free.?block"),
    ("Java / OOP", r"java|class|interface|inheritance|polymorph|overrid|encapsul|abstract|Object|FileInputStream|increment|main\("),
    ("C++", r"c\+\+|iostream|switch statement"),
    ("Data Structures", r"binary tree|quad.?tree|hash table|queue|complexity|time complexity|O\("),
    ("Database", r"SQL|foreign key|primary key|CASCADE|relation|schema|HOTEL|ROOM|view|participation|DISTINCT"),
    ("Networking", r"TCP|SSH|port|IPv4|OSI|application layer|encapsulation|switch|MAC|access list|OSPF|PPP|LLC|data link"),
    ("Web Development", r"HTML|CSS|Javascript|JSON|\bform\b|<form|opacity|border-radius|let\b|const\b"),
    ("Android", r"android|APK|Dalvik|activity|onCreate|layout|View|Fragment|mobile device"),
    ("Software Testing", r"testing|coverage|integration test|precision|recall|test report|decision coverage|verif"),
    ("Software Architecture", r"architectural|MVC|client server|notation|performance|robustness"),
    ("Project Management", r"project|functional organization|affinity|Pareto|validation|temporary endeavor|Six sigma|CMMI|CASE"),
    ("AI / ML", r"artificial intelligence|agent|informed search|local search|ensemble|lasso|boosting|bagging|overfit|gradient descent|preprocessing|big data|velocity"),
    ("Security", r"confidentiality|integrity|digital signature|spam|professional ethics|risk management"),
    ("Software Engineering", r"SDLC|requirement|software tool|version control|logical error|bootstrap compiler"),
]


def classify(text: str) -> str:
    for topic, pat in TOPIC_RULES:
        if re.search(pat, text, re.I):
            return topic
    return "Software Engineering"


def concept_line(topic: str, answer: str, options: list[dict]) -> str:
    correct = next((o for o in options if o["key"] == answer), None)
    if correct:
        t = correct["text"]
        return f"Key idea ({topic}): {t[:120]}{'…' if len(t) > 120 else ''}"
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
    for n in range(1, 101):
        if n not in found:
            skipped.append(f"Q{n}: not parsed from PDF")

    return questions, skipped


def main() -> None:
    if not RAW_PATH.exists():
        print(f"Missing {RAW_PATH}. Run extract_model1_pdf.py first.")
        return
    questions, skipped = build_questions()
    payload = {
        "title": "MoEE Software Engineering Model Exam 1",
        "source": "MODEL1.pdf — MoEE Exit Exam (Dagmawi Abate model)",
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
