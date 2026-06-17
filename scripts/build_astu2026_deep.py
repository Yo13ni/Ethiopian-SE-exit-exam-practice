"""Generate deep explanations for ASTU 2026 model exam rounds only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from astu2026_deep_builder import build_deep_entry  # noqa: E402

EXAM_IDS = ("astu2026r1", "astu2026r2", "astu2026r3")


def main() -> None:
    catalog = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
    by_id = {e["id"]: e for e in catalog["exams"]}
    total = 0

    for exam_id in EXAM_IDS:
        exam = by_id[exam_id]
        q_path = ROOT / exam["questionsPath"]
        out_path = ROOT / exam["deepPath"]
        data = json.loads(q_path.read_text(encoding="utf-8"))
        out: dict[str, dict] = {}

        for q in data["questions"]:
            num = str(q["examNumber"])
            out[num] = build_deep_entry(q)
            total += 1

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  {exam_id}: {len(out)} explanations -> {out_path.relative_to(ROOT)}")

    print(f"Done — {total} explanations for {len(EXAM_IDS)} ASTU 2026 rounds.")


if __name__ == "__main__":
    main()
