"""Add MoEE blueprint cognitiveLevel to all exam question banks."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from cognitive_classifier import COGNITIVE_LEVELS, classify_question, normalize_level

SUMMARY_PATH = ROOT / "data" / "cognitive_classification_summary.json"


def process_exam(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    exam_id = path.parent.name
    level_counts: Counter[str] = Counter()
    topic_level: dict[str, Counter[str]] = defaultdict(Counter)
    changed = 0

    for q in data.get("questions", []):
        old = q.get("cognitiveLevel")
        level = classify_question(q)
        if old != level:
            changed += 1
        q["cognitiveLevel"] = level
        level_counts[level] += 1
        topic_level[q.get("topic", "General")][level] += 1

    if changed:
        rev = data.get("dataRevision", 0)
        data["dataRevision"] = rev + 1 if isinstance(rev, int) else 1

    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return {
        "examId": exam_id,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "total": len(data.get("questions", [])),
        "changed": changed,
        "levels": dict(level_counts),
        "byTopic": {t: dict(c) for t, c in sorted(topic_level.items())},
    }


def main() -> None:
    exam_files = sorted((ROOT / "data" / "exams").glob("*/questions.json"))
    if not exam_files:
        print("No exam question files found.")
        return

    results = [process_exam(p) for p in exam_files]
    grand = Counter()
    for r in results:
        grand.update(r["levels"])

    summary = {
        "generatedOn": date.today().isoformat(),
        "blueprint": "MoEE Feb 2024 — Software Engineering & Computing Technology",
        "cognitiveLevels": list(COGNITIVE_LEVELS),
        "totalQuestions": sum(r["total"] for r in results),
        "examCount": len(results),
        "overallDistribution": dict(grand),
        "exams": results,
    }
    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Classified {summary['totalQuestions']} questions across {len(results)} exams")
    print("\nOverall cognitive level distribution:")
    for level in COGNITIVE_LEVELS:
        n = grand.get(level, 0)
        pct = 100 * n / summary["totalQuestions"] if summary["totalQuestions"] else 0
        print(f"  {level:20} {n:4}  ({pct:5.1f}%)")
    print(f"\nWrote summary -> {SUMMARY_PATH.relative_to(ROOT)}")
    for r in results:
        print(f"  {r['examId']:12} {r['total']:3} q  ({r['changed']} updated)")


if __name__ == "__main__":
    main()
