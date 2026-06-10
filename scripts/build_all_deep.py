"""Regenerate all exam deep_explanations.json in unified BDU+model1 style."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from unified_deep_builder import build_deep_entry  # noqa: E402

CATALOG = ROOT / "data" / "catalog.json"


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    total = 0
    shallow_fixed = 0

    for exam in catalog.get("exams", []):
        exam_id = exam["id"]
        q_path = ROOT / exam["questionsPath"]
        out_path = ROOT / exam["deepPath"]
        data = json.loads(q_path.read_text(encoding="utf-8"))
        out: dict[str, dict] = {}

        for q in data["questions"]:
            num = str(q["examNumber"])
            entry = build_deep_entry(q, exam_id)
            out[num] = entry
            total += 1

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  {exam_id}: {len(out)} explanations -> {out_path.relative_to(ROOT)}")

    print(f"Done — {total} explanations across {len(catalog.get('exams', []))} exams.")


if __name__ == "__main__":
    main()
