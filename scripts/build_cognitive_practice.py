"""Build data/cognitive_practice.json — questions grouped by MoEE cognitive level."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "cognitive_practice.json"

LEVELS = (
    "Remembering",
    "Understanding",
    "Application",
    "Analysis",
    "Evaluation",
    "Creation/Synthesis",
)

LEVEL_META = {
    "Remembering": {
        "slug": "remembering",
        "description": "Recall facts, definitions, terms, and basic concepts.",
    },
    "Understanding": {
        "slug": "understanding",
        "description": "Explain, describe, and interpret ideas in your own words.",
    },
    "Application": {
        "slug": "application",
        "description": "Apply knowledge to solve problems, trace code, and use tools.",
    },
    "Analysis": {
        "slug": "analysis",
        "description": "Compare, differentiate, and break down complex scenarios.",
    },
    "Evaluation": {
        "slug": "evaluation",
        "description": "Assess options, judge trade-offs, and apply professional ethics.",
    },
    "Creation/Synthesis": {
        "slug": "creation-synthesis",
        "description": "Design, develop, and construct solutions to open-ended problems.",
    },
}


def main() -> None:
    groups: dict[str, list[dict]] = defaultdict(list)
    total = 0

    for path in sorted((ROOT / "data" / "exams").glob("*/questions.json")):
        exam_id = path.parent.name
        data = json.loads(path.read_text(encoding="utf-8"))
        exam_title = data.get("title") or exam_id

        for q in data.get("questions", []):
            level = q.get("cognitiveLevel") or "Understanding"
            if level not in LEVELS:
                level = "Understanding"
            exam_number = q.get("examNumber", q.get("id"))
            entry = {
                "practiceKey": f"{exam_id}:{exam_number}",
                "sourceExamId": exam_id,
                "examId": exam_id,
                "examTitle": exam_title,
                "examNumber": exam_number,
                "topic": q.get("topic", "General"),
                "text": q.get("text", ""),
                "options": q.get("options", []),
                "answer": q.get("answer", ""),
                "concept": q.get("concept", ""),
                "cognitiveLevel": level,
            }
            groups[level].append(entry)
            total += 1

    levels_out = []
    for name in LEVELS:
        meta = LEVEL_META[name]
        qs = sorted(groups[name], key=lambda x: (x["examId"], x["examNumber"] or 0))
        levels_out.append({
            "name": name,
            "slug": meta["slug"],
            "description": meta["description"],
            "count": len(qs),
            "questions": qs,
        })

    bundle = {
        "version": 1,
        "generatedOn": date.today().isoformat(),
        "blueprint": "MoEE Feb 2024 — Software Engineering & Computing Technology",
        "totalQuestions": total,
        "levels": levels_out,
    }
    OUT.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} — {total} questions in {len(levels_out)} levels")
    for lv in levels_out:
        print(f"  {lv['name']:20} {lv['count']:4}")


if __name__ == "__main__":
    main()
