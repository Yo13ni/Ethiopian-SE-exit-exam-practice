import json
from pathlib import Path

ROOT = Path(__file__).parent
pages = json.loads((ROOT / "data/exams/aau/raw_ocr.json").read_text(encoding="utf-8"))
lines = []
for p in pages:
    q = p["parsed"]
    if len(q.get("options", [])) >= 3 and len(q.get("text", "")) > 25:
        lines.append(f"--- Q{q['examNumber']} page {p['page']} ---")
        lines.append(q["text"][:300])
        for o in q["options"][:4]:
            lines.append(f"  {o['key']}. {o['text'][:100]}")
        lines.append("")
(ROOT.parent / "aau_questions_preview.txt").write_text("\n".join(lines), encoding="utf-8")
print(len([1 for p in pages if len(p["parsed"].get("options",[]))>=3]), "questions")
