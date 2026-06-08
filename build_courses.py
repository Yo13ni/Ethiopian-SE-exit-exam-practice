"""Aggregate exam questions by course/topic into per-course practice banks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent
CATALOG = ROOT / "data" / "catalog.json"
COURSES = ROOT / "data" / "courses.json"
OUT_DIR = ROOT / "data" / "courses"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    catalog = load_json(CATALOG)
    courses_meta = load_json(COURSES)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    topic_to_course: dict[str, str] = {}
    course_defs: dict[str, dict] = {}
    for course in courses_meta["courses"]:
        course_defs[course["id"]] = course
        for topic in course["topics"]:
            topic_to_course[topic] = course["id"]

    buckets: dict[str, list[dict]] = {cid: [] for cid in course_defs}
    seen: dict[str, set[str]] = {cid: set() for cid in course_defs}

    for exam in catalog["exams"]:
        exam_id = exam["id"]
        qpath = ROOT / exam["questionsPath"]
        if not qpath.exists():
            continue
        payload = load_json(qpath)
        focus = payload.get("focusGuide") or {}

        for q in payload.get("questions", []):
            topic = q.get("topic", "General")
            course_id = topic_to_course.get(topic)
            if not course_id:
                continue

            text_key = " ".join(q.get("text", "").split()).lower()
            dedup_key = f"{text_key}|{q.get('answer', '')}"
            if dedup_key in seen[course_id]:
                continue
            seen[course_id].add(dedup_key)

            entry = dict(q)
            entry["sourceExamId"] = exam_id
            entry["sourceQuestionId"] = q.get("id")
            entry["sourceExamTitle"] = exam.get("title", exam_id)
            buckets[course_id].append(entry)

    summary = []
    enriched_courses = []
    for course in courses_meta["courses"]:
        cid = course["id"]
        questions = buckets[cid]
        for i, q in enumerate(questions, start=1):
            q["id"] = i

        focus_guide = {}
        for topic in course["topics"]:
            for exam in catalog["exams"]:
                qpath = ROOT / exam["questionsPath"]
                if not qpath.exists():
                    continue
                fg = load_json(qpath).get("focusGuide") or {}
                if topic in fg:
                    focus_guide[topic] = fg[topic]

        title = course.get("shortTitle") or course["title"]
        out = {
            "title": f"{title} — Course Practice",
            "courseId": cid,
            "topics": course["topics"],
            "total": len(questions),
            "focusGuide": focus_guide,
            "questions": questions,
            "dataRevision": 1,
        }

        course_dir = OUT_DIR / cid
        course_dir.mkdir(parents=True, exist_ok=True)
        out_path = course_dir / "questions.json"
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        summary.append((cid, len(questions), out_path))

        enriched = dict(course)
        enriched["questionsPath"] = f"data/courses/{cid}/questions.json"
        enriched["questionCount"] = len(questions)
        enriched["dataRevision"] = out["dataRevision"]
        enriched_courses.append(enriched)

    courses_meta["courses"] = enriched_courses
    COURSES.write_text(json.dumps(courses_meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Built course question banks:")
    for cid, count, path in summary:
        print(f"  {cid}: {count} questions -> {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
