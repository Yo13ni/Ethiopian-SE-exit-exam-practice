"""Build BDU Model Exit Exam questions.json from OCR pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

from bdu_answer_solver import solve_answer
from bdu_answers import ANSWERS as BDU_ANSWERS
from bdu_exam_data import FOCUS_GUIDE, MANUAL_OVERRIDES
from bdu_parser import is_promo, parse_bdu_page

ROOT = Path(__file__).parent
RAW_PATH = ROOT / "data" / "exams" / "bdu" / "raw_ocr.json"
MATCHED_PATH = ROOT / "data" / "exams" / "bdu" / "matched_answers.json"
OUT_PATH = ROOT / "data" / "exams" / "bdu" / "questions.json"

TOPIC_RULES: list[tuple[str, str]] = [
    ("Software Architecture", r"software architecture|quality scenario|ATAM|layered architecture|coupling|cohesion|microservice"),
    ("Software Testing", r"software test|tester|test process|coverage|traceability|defect|regression test"),
    ("Database", r"SQL|relation schema|functional dependency|foreign key|normal form|normalization|entity|ER diagram|cardinality"),
    ("Android", r"android|activity|intent|APK|manifest|ViewGroup|layout|service|content provider|onCreate"),
    ("Java / OOP", r"java|interface|abstract class|constructor|inheritance|polymorphism|UML|try.?catch|garbage collection|OOP"),
    ("Web Development", r"CSS|HTML|JavaScript|javascript|PHP|HTTP request|DOM|GET method|POST method|cookie|web page"),
    ("Networking", r"OSI|TCP|UDP|subnet|firewall|router|switch|hub|IPv4|HTTP|SMTP|DNS|packet|CORS|REST|WAN|LAN|Ethernet"),
    ("Security", r"confidentiality|integrity|authorization|authentication|cyber security|encryption|digital signature|malware|virus|worm"),
    ("Project Management", r"project|agile|waterfall|spiral|incremental|Tuckman|ROI|stakeholder|WBS|critical path|scrum"),
    ("AI / ML", r"machine learning|supervised|unsupervised|reinforcement|data mining|search algorithm|A\*|heuristic|BFS|DFS|UCS|Dijkstra"),
    ("Operating Systems", r"operating system|process state|deadlock|banker|memory management|page replacement|scheduling|fork|thread|swapping|paging"),
    ("C++", r"C\+\+|#include|iostream|cout|for loop|identifier|void solve|compiling|linking|\bnew\b|\bdelete\b"),
    ("Data Structures", r"time complexity|O\(|binary search|selection sort|linked.?list|tree|stack|queue|asymptotic|Big-Oh|Big-Omega|Theta|sort algorithm|circular"),
    ("Software Engineering", r"requirement|SRS|maintenance|evolution|SDLC|software model|design principle|UML element"),
]


def classify(text: str) -> str:
    for topic, pat in TOPIC_RULES:
        if re.search(pat, text, re.I):
            return topic
    return "General"


def concept_line(topic: str, answer: str | None, options: list[dict]) -> str:
    if not answer:
        return f"Review this {topic} concept in your notes."
    correct = next((o for o in options if o["key"] == answer), None)
    if correct:
        return f"Key idea ({topic}): {correct['text']}"
    return f"Key idea ({topic}): answer {answer}"


def load_matched() -> dict[int, str]:
    if not MATCHED_PATH.exists():
        return {}
    raw = json.loads(MATCHED_PATH.read_text(encoding="utf-8"))
    return {int(k): v for k, v in raw.items()}


def build_questions() -> tuple[list[dict], list[str]]:
    pages = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    matched = load_matched()
    questions: list[dict] = []
    skipped: list[str] = []

    for page in pages:
        pnum = page["page"]
        raw = page.get("raw", "")

        if is_promo(raw) or pnum > 99:
            skipped.append(f"page {pnum}: promo/footer")
            continue

        parsed = parse_bdu_page(raw, pnum)
        exam_num = pnum

        override = MANUAL_OVERRIDES.get(exam_num, {})
        text = override.get("text") or parsed["text"]
        options = override.get("options") or parsed["options"]

        if len(text) < 10 and exam_num not in MANUAL_OVERRIDES:
            skipped.append(f"page {pnum} (Q{exam_num}): stem too short — {text[:40]!r}")
            continue

        clear_opts = sum(1 for o in options if "(option unclear" not in o["text"] and len(o["text"]) > 2)
        if clear_opts < 2 and exam_num not in MANUAL_OVERRIDES:
            skipped.append(f"page {pnum} (Q{exam_num}): fewer than 2 parseable options")
            continue

        topic = override.get("topic") or classify(text + " " + " ".join(o["text"] for o in options))
        answer = (
            override.get("answer")
            or matched.get(exam_num)
            or BDU_ANSWERS.get(exam_num)
            or solve_answer(exam_num, text, options, topic)
        )
        if not answer:
            skipped.append(f"page {pnum} (Q{exam_num}): could not determine answer")
            continue

        questions.append({
            "examNumber": exam_num,
            "id": len(questions) + 1,
            "topic": topic,
            "text": text,
            "options": options,
            "answer": answer,
            "concept": concept_line(topic, answer, options),
        })

    return questions, skipped


def main() -> None:
    if not RAW_PATH.exists():
        print(f"Missing {RAW_PATH}. Run extract_bdu_ocr.py first.")
        return
    questions, skipped = build_questions()
    payload = {
        "title": "BDU Model Exit Exam",
        "source": "Bahir Dar University (BDU) Model Exit Exam — Moodle OCR",
        "total": len(questions),
        "focusGuide": FOCUS_GUIDE,
        "questions": questions,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(questions)} questions -> {OUT_PATH}")
    if skipped:
        print(f"Skipped {len(skipped)}:")
        for s in skipped[:25]:
            print(f"  - {s}")
        if len(skipped) > 25:
            print(f"  ... and {len(skipped) - 25} more")


if __name__ == "__main__":
    main()
