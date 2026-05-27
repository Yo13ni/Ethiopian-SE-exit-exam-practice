"""Build deep explanations for MoEE Model Exam 1."""

from __future__ import annotations

import json
from pathlib import Path

from model1_deep_builder import build_deep_entry, enrich_with_concept

ROOT = Path(__file__).parent
QUESTIONS_PATH = ROOT / "data" / "exams" / "model1" / "questions.json"
OUT_PATH = ROOT / "data" / "exams" / "model1" / "deep_explanations.json"


def main() -> None:
    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for q in data["questions"]:
        num = str(q["examNumber"])
        out[num] = enrich_with_concept(q, build_deep_entry(q))
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(out)} deep explanations -> {OUT_PATH}")


if __name__ == "__main__":
    main()
