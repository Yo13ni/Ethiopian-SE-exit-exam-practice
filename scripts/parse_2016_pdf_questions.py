"""Parse Question N blocks from OCR pages and compare to web 2016 bank."""

from __future__ import annotations

import json
import re
from pathlib import Path

WEB = Path(__file__).resolve().parent.parent / "data" / "exams" / "2016" / "questions.json"
OCR = Path(__file__).resolve().parent.parent / "data" / "exams" / "2016" / "pdf_ocr_text.json"


def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_questions_from_ocr(pages: list[str]) -> dict[int, str]:
    blob = "\n".join(pages)
    # Split on "Question N" headers (Moodle export)
    parts = re.split(r"(?i)question\s+(\d{1,3})\b", blob)
    out: dict[int, str] = {}
    i = 1
    while i + 1 < len(parts):
        num = int(parts[i])
        body = parts[i + 1]
        # trim navigation noise
        body = re.split(r"(?i)(clear my choice|previous page|next page|quiz navigation)", body)[0]
        if 1 <= num <= 100:
            out[num] = body.strip()
        i += 2
    return out


def word_overlap(a: str, b: str) -> float:
    aw = {w for w in normalize(a).split() if len(w) > 2}
    bw = {w for w in normalize(b).split() if len(w) > 2}
    if not aw:
        return 0.0
    return len(aw & bw) / len(aw)


def main() -> None:
    web = json.loads(WEB.read_text(encoding="utf-8"))
    web_by_num = {q["examNumber"]: q for q in web["questions"]}

    if not OCR.exists():
        print("Run compare_2016_pdf.py first to generate OCR text.")
        return

    pages = json.loads(OCR.read_text(encoding="utf-8"))
    pdf_q = parse_questions_from_ocr(pages)

    print(f"OCR pages: {len(pages)}")
    print(f"PDF questions parsed: {len(pdf_q)} (nums: {sorted(pdf_q)[:20]}... max {max(pdf_q) if pdf_q else 0})")
    print(f"Web questions: {len(web_by_num)}")
    print()

    in_pdf_not_web = sorted(set(pdf_q) - set(web_by_num))
    in_web_not_pdf = sorted(set(web_by_num) - set(pdf_q))
    print(f"In PDF only: {in_pdf_not_web}")
    print(f"In web only (not found in OCR yet): {len(in_web_not_pdf)} questions")
    print()

    match = partial = mismatch = 0
    issues = []
    for num in sorted(set(web_by_num) & set(pdf_q)):
        w = web_by_num[num]
        pdf_text = pdf_q[num]
        score = word_overlap(w["text"], pdf_text)
        if score >= 0.5:
            match += 1
            status = "match"
        elif score >= 0.3:
            partial += 1
            status = "partial"
        else:
            mismatch += 1
            status = "mismatch"
        if status != "match":
            issues.append((num, status, score, w["text"][:90], pdf_text[:90]))

    print(f"Compared {match + partial + mismatch} questions present in both:")
    print(f"  match: {match}, partial: {partial}, mismatch: {mismatch}")
    print()
    print("Issues (web vs PDF stem):")
    for num, status, score, wstem, pstem in issues[:40]:
        print(f"  Q{num} [{status}] overlap={score:.2f}")
        print(f"    WEB: {wstem}")
        print(f"    PDF: {pstem}")
        print()


if __name__ == "__main__":
    main()
