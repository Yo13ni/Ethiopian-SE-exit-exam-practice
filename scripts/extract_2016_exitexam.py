"""Extract all 100 questions from 2016-exitexam.pdf via OCR."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import easyocr
import fitz

PDF = Path(
    r"c:\Users\Hp\AppData\Roaming\Cursor\User\workspaceStorage"
    r"\d5a59c4bacc7f49b4b12a545283c3af4\pdfs"
    r"\33f1d4d4-0f3a-465b-9e8a-c16438ad9284\2016-exitexam.pdf"
)
OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "exams" / "2016"
OCR_PAGES = OUT_DIR / "exitexam_ocr_pages.json"
EXTRACTED = OUT_DIR / "exitexam_extracted.json"


def ocr_all(resume: bool = True) -> list[str]:
    pages: list[str] = []
    if resume and OCR_PAGES.exists():
        pages = json.loads(OCR_PAGES.read_text(encoding="utf-8"))
        print(f"Resuming from {len(pages)} cached pages", file=sys.stderr)

    reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    doc = fitz.open(PDF)
    start = len(pages)
    for i in range(start, doc.page_count):
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(1.8, 1.8))
        lines = reader.readtext(pix.tobytes("png"), detail=0, paragraph=True)
        text = "\n".join(lines)
        pages.append(text)
        OCR_PAGES.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"OCR {i + 1}/{doc.page_count}", file=sys.stderr)
    return pages


def parse_page(page_num: int, text: str) -> dict:
    """Parse one Moodle question screenshot."""
    qnum = page_num
    m = re.search(r"(?i)question\s+(\d{1,3})\b", text)
    if m:
        qnum = int(m.group(1))

    body = text
    for marker in (r"(?i)flag question", r"(?i)marked out of"):
        m2 = re.search(marker, body)
        if m2:
            body = body[m2.end():]
            break

    # Split options a. b. c. d.
    opt_parts = re.split(r"(?<=\s)(?=[a-d]\.\s)", body, flags=re.I)
    stem = opt_parts[0].strip()
    stem = re.sub(r"(?i)^select one:?\s*", "", stem).strip()
    stem = re.sub(r"\s+", " ", stem)

    options: list[dict] = []
    for part in opt_parts[1:]:
        om = re.match(r"([a-d])\.\s*(.+)", part.strip(), re.I | re.S)
        if om:
            opt_text = om.group(2).strip()
            opt_text = re.split(r"(?i)(clear my choice|previous page|next page)", opt_text)[0].strip()
            opt_text = re.sub(r"\s+", " ", opt_text)
            options.append({"key": om.group(1).upper(), "text": opt_text})

    if len(options) < 4:
        # fallback: find a. ... b. ... in full text
        opts = re.findall(r"(?i)\b([a-d])\.\s*([^\n]+?)(?=\s+[a-d]\.\s|\Z)", body, re.S)
        if len(opts) >= 4:
            options = [{"key": k.upper(), "text": re.sub(r"\s+", " ", t.strip())} for k, t in opts[:4]]

    return {
        "examNumber": qnum,
        "page": page_num,
        "text": stem,
        "options": options,
        "rawOcr": text,
    }


def main() -> None:
    pages = ocr_all(resume=True)
    questions = [parse_page(i + 1, t) for i, t in enumerate(pages)]
    EXTRACTED.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Extracted {len(questions)} questions -> {EXTRACTED}")


if __name__ == "__main__":
    main()
