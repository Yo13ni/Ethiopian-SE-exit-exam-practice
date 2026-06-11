"""Compare web questions.json stems to OCR page order."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OCR = json.loads((ROOT / "data/exams/2016/exitexam_ocr_pages.json").read_text(encoding="utf-8"))
WEB = json.loads((ROOT / "data/exams/2016/questions.json").read_text(encoding="utf-8"))

# Parse OCR pages -> question number -> first 80 chars of stem
ocr_by_num: dict[int, str] = {}
current_num = None
blob = ""
for i, page in enumerate(OCR):
    m = re.search(r"(?i)question\s+(\d{1,3})\b", page)
    if m:
        if current_num and blob:
            ocr_by_num[current_num] = blob.strip()[:120]
        current_num = int(m.group(1))
        blob = page
    else:
        blob += "\n" + page
if current_num and blob:
    ocr_by_num[current_num] = blob.strip()[:120]

# Normalize for overlap check
def norm(s):
    s = re.sub(r"(?i)(not yet answered|marked out.*?|flag question)", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()

def overlap(a, b):
    aw = {w for w in norm(a).split() if len(w) > 3}
    bw = {w for w in norm(b).split() if len(w) > 3}
    if not aw:
        return 0.0
    return len(aw & bw) / len(aw)

web_by_num = {q["examNumber"]: q for q in WEB["questions"]}

print(f"OCR questions parsed: {len(ocr_by_num)} (max {max(ocr_by_num)})")
print(f"Web questions: {len(web_by_num)}")
print()
mismatch = []
for num in sorted(set(ocr_by_num) & set(web_by_num)):
    score = overlap(web_by_num[num]["text"], ocr_by_num[num])
    if score < 0.35:
        mismatch.append((num, score, web_by_num[num]["text"][:70], ocr_by_num[num][:70]))

print(f"Mismatched stems (overlap < 0.35): {len(mismatch)}")
for num, score, w, o in mismatch:
    print(f"\nQ{num} overlap={score:.2f}")
    print(f"  WEB: {w}")
    print(f"  OCR: {o}")
