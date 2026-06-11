"""OCR pre-rendered 2016 exit exam pages and parse questions."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import easyocr

PAGES_DIR = Path(__file__).resolve().parent.parent / "data" / "exams" / "2016" / "exitexam_pages"
OUT = Path(__file__).resolve().parent.parent / "data" / "exams" / "2016" / "exitexam_extracted.json"
CACHE = Path(__file__).resolve().parent.parent / "data" / "exams" / "2016" / "exitexam_ocr_pages.json"


def parse_page(page_num: int, text: str) -> dict:
    qnum = page_num
    m = re.search(r"(?i)question\s+(\d{1,3})\b", text)
    if m:
        qnum = int(m.group(1))

    body = text
    fm = re.search(r"(?i)flag question", body)
    if fm:
        body = body[fm.end():]

    opt_parts = re.split(r"(?<=\s)(?=[a-d]\.\s)", body, flags=re.I)
    stem = re.sub(r"\s+", " ", opt_parts[0].strip())

    options: list[dict] = []
    for part in opt_parts[1:]:
        om = re.match(r"([a-d])\.\s*(.+)", part.strip(), re.I | re.S)
        if om:
            t = re.sub(r"\s+", " ", om.group(2).strip())
            options.append({"key": om.group(1).upper(), "text": t})

    if len(options) < 4:
        opts = re.findall(r"(?i)([a-d])\.\s*([^\n]+)", body)
        if len(opts) >= 4:
            options = [{"key": k.upper(), "text": re.sub(r"\s+", " ", t.strip())} for k, t in opts[:4]]

    return {"examNumber": qnum, "page": page_num, "text": stem, "options": options}


def main() -> None:
    imgs = sorted(PAGES_DIR.glob("q*.png"))
    cached: list[str] = []
    if CACHE.exists():
        cached = json.loads(CACHE.read_text(encoding="utf-8"))

    reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    texts = list(cached)
    for i in range(len(cached), len(imgs)):
        lines = reader.readtext(str(imgs[i]), detail=0, paragraph=True)
        text = "\n".join(lines)
        texts.append(text)
        CACHE.write_text(json.dumps(texts, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{i + 1}/{len(imgs)}", file=sys.stderr)

    questions = [parse_page(i + 1, t) for i, t in enumerate(texts)]
    OUT.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(questions)} questions")


if __name__ == "__main__":
    main()
