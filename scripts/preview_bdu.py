import json
from pathlib import Path
from bdu_parser import parse_bdu_page, is_promo

ROOT = Path(__file__).resolve().parent.parent
pages = json.loads((ROOT / "data/exams/bdu/raw_ocr.json").read_text(encoding="utf-8"))
for p in pages:
    if is_promo(p["raw"]) or p["page"] > 99:
        continue
    parsed = parse_bdu_page(p["raw"], p["page"])
    clear = sum(
        1 for o in parsed["options"]
        if "(option unclear" not in o["text"] and len(o["text"]) > 2
    )
    if clear >= 2:
        print(f"Q{p['page']:3d} [{clear} opts] {parsed['text'][:80]}")
    else:
        print(f"Q{p['page']:3d} [SKIP {clear}] {parsed['text'][:60]}")
