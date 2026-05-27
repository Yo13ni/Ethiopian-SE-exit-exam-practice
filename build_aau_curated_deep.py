"""Build curated deep explanations for AAU Model Exit Exam."""

from __future__ import annotations

import json
from pathlib import Path

from aau_deep_builder import build_deep_entry

ROOT = Path(__file__).parent
QUESTIONS_PATH = ROOT / "data" / "exams" / "aau" / "questions.json"
OUT_PATH = ROOT / "data" / "exams" / "aau" / "deep_explanations.json"


def main() -> None:
    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    missing = []
    for q in data["questions"]:
        num = str(q["examNumber"])
        try:
            out[num] = build_deep_entry(q)
        except KeyError:
            missing.append(num)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(out)} deep explanations -> {OUT_PATH}")
    if missing:
        print(f"Missing bank entries: {missing}")


if __name__ == "__main__":
    main()
