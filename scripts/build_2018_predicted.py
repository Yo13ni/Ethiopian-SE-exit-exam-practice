"""Build predicted 2018 exit exam JSON (questions + deep explanations)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from exam2018_data import FOCUS_GUIDE, PREDICTED_2018_QUESTIONS  # noqa: E402
from generic_deep_builder import build_deep_entry, enrich_with_concept  # noqa: E402

OUT_DIR = ROOT / "data" / "exams" / "2018"
QUESTIONS_PATH = OUT_DIR / "questions.json"
DEEP_PATH = OUT_DIR / "deep_explanations.json"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    questions = []
    for i, raw in enumerate(PREDICTED_2018_QUESTIONS, start=1):
        q = dict(raw)
        q["examNumber"] = i
        q["id"] = i
        questions.append(q)

    payload = {
        "title": "2018 Software Engineering Exit Exam (Predicted)",
        "source": "Pattern-based prediction from 2015–2017 exams + MoEE blueprint / Exit Notes",
        "total": len(questions),
        "timeLimitHours": 3,
        "dataRevision": 1,
        "predicted": True,
        "focusGuide": FOCUS_GUIDE,
        "questions": questions,
    }
    QUESTIONS_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {QUESTIONS_PATH} ({len(questions)} questions)")

    deep: dict[str, dict] = {}
    for q in questions:
        num = str(q["examNumber"])
        deep[num] = enrich_with_concept(q, build_deep_entry(q))
        deep[num]["source"] = "offline-deep"

    DEEP_PATH.write_text(json.dumps(deep, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {DEEP_PATH} ({len(deep)} entries)")

    from collections import Counter

    counts = Counter(q["topic"] for q in questions)
    print("\nTopic distribution:")
    for topic, n in counts.most_common():
        print(f"  {topic}: {n}")


if __name__ == "__main__":
    main()
