import json
from pathlib import Path
from bdu_parser import parse_bdu_page, is_promo

pages = json.loads(Path("data/exams/bdu/raw_ocr.json").read_text(encoding="utf-8"))
out = []
for p in pages:
    if is_promo(p["raw"]) or p["page"] > 99:
        continue
    parsed = parse_bdu_page(p["raw"], p["page"])
    out.append({
        "n": p["page"],
        "text": parsed["text"],
        "options": {o["key"]: o["text"] for o in parsed["options"]},
    })
Path("data/exams/bdu/preview_all.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(len(out), "questions exported")
