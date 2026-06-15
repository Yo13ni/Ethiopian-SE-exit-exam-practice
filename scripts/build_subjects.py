"""Build data/subjects.json — all exam questions grouped by subject/topic."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "catalog.json"
OUT = ROOT / "data" / "subjects.json"

EXAM_ORDER = ["2015", "2016", "2017", "2018", "aau", "bdu", "astu", "model1", "moe2025"]

SUBJECT_ORDER = [
    "Operating Systems",
    "Java / OOP",
    "C++",
    "Data Structures",
    "Database",
    "Networking",
    "Web Development",
    "Android",
    "Software Testing",
    "Software Engineering",
    "Software Maintenance",
    "Software Architecture",
    "Project Management",
    "AI / ML",
    "Security",
    "Fundamentals of Programming",
    "General",
]


def topic_slug(topic: str) -> str:
    s = topic.lower().replace(" / ", "-").replace("/", "-")
    out = []
    for ch in s:
        out.append(ch if ch.isalnum() or ch == "-" else "-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def exam_sort_key(exam_id: str) -> int:
    try:
        return EXAM_ORDER.index(exam_id)
    except ValueError:
        return 999


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    exams_by_id = {e["id"]: e for e in catalog.get("exams", [])}

    focus_guide: dict[str, str] = {}
    groups: dict[str, list[dict]] = defaultdict(list)
    total = 0

    for exam_id in EXAM_ORDER:
        exam = exams_by_id.get(exam_id)
        if not exam:
            continue
        q_path = ROOT / exam["questionsPath"]
        if not q_path.exists():
            continue
        q_data = json.loads(q_path.read_text(encoding="utf-8"))
        exam_title = q_data.get("title") or exam.get("title") or exam_id

        for topic, guide in (q_data.get("focusGuide") or {}).items():
            if topic not in focus_guide and guide:
                focus_guide[topic] = guide

        for q in q_data.get("questions", []):
            topic = q.get("topic") or "General"
            groups[topic].append({
                "examId": exam_id,
                "examTitle": exam_title,
                "examNumber": q.get("examNumber", q.get("id")),
                "topic": topic,
                "text": q.get("text", ""),
                "options": q.get("options", []),
                "answer": q.get("answer", ""),
                "concept": q.get("concept", ""),
            })
            total += 1

    subjects = []
    seen = set()
    for name in SUBJECT_ORDER:
        if name not in groups:
            continue
        seen.add(name)
        qs = sorted(
            groups[name],
            key=lambda q: (exam_sort_key(q["examId"]), q.get("examNumber") or 0),
        )
        subjects.append({
            "name": name,
            "slug": topic_slug(name),
            "count": len(qs),
            "guide": focus_guide.get(name, ""),
            "questions": qs,
        })

    for name in sorted(groups.keys()):
        if name in seen:
            continue
        qs = sorted(
            groups[name],
            key=lambda q: (exam_sort_key(q["examId"]), q.get("examNumber") or 0),
        )
        subjects.append({
            "name": name,
            "slug": topic_slug(name),
            "count": len(qs),
            "guide": focus_guide.get(name, ""),
            "questions": qs,
        })

    bundle = {
        "version": 1,
        "totalQuestions": total,
        "examCount": len(EXAM_ORDER),
        "focusGuide": focus_guide,
        "subjects": subjects,
    }
    OUT.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT} — {total} questions in {len(subjects)} subjects")
    for s in subjects:
        print(f"  {s['name']}: {s['count']}")


if __name__ == "__main__":
    main()
