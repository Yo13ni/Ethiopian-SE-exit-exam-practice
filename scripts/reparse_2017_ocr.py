"""Re-parse existing 2017 raw OCR with improved parser (no re-OCR)."""

from __future__ import annotations

import json
from pathlib import Path

from exam2017_parser import parse_2017_page

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "exams" / "2017" / "raw_ocr.json"
MAP_PATH = ROOT / "data" / "exams" / "2017" / "number_map.json"


def load_number_map() -> dict[int, int]:
    if not MAP_PATH.exists():
        return {}
    rows = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    return {r["page"]: r["examNumber"] for r in rows if r.get("examNumber")}


def main() -> None:
    pages = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    num_map = load_number_map()
    for page in pages:
        raw = page.get("raw", "")
        parsed = parse_2017_page(raw, page.get("page", 0))
        mapped = num_map.get(page.get("page"))
        if mapped:
            parsed["examNumber"] = mapped
        page["parsed"] = parsed

    RAW_PATH.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")

    by_num: dict[int, dict] = {}
    for p in pages:
        parsed = p["parsed"]
        n = parsed["examNumber"]
        if len(parsed.get("text", "")) > 15 and len(parsed.get("options", [])) >= 2:
            prev = by_num.get(n)
            score = len(parsed["text"]) + sum(len(o["text"]) for o in parsed["options"])
            prev_score = 0
            if prev:
                prev_score = len(prev["text"]) + sum(len(o["text"]) for o in prev["options"])
            if not prev or score > prev_score:
                by_num[n] = parsed

    print(f"Re-parsed: {len(by_num)} unique questions with stem + 2+ options")


if __name__ == "__main__":
    main()
