"""Extract text from ASTU Software Engineering MCQ PDF."""

from __future__ import annotations

import json
import re
from pathlib import Path

import fitz

PDF = Path(
    r"c:\Users\Hp\AppData\Roaming\Cursor\User\workspaceStorage"
    r"\87ef23a07efdc78cd48c499e89b4651a\pdfs"
    r"\685f7747-aead-4f7b-9257-923d382ad5da"
    r"\ASTU.Software Eng.pdf"
)
OUT_RAW = Path(__file__).parent / "data" / "exams" / "astu" / "raw_text.json"


def extract_full_text() -> str:
    doc = fitz.open(str(PDF))
    pages = [doc[i].get_text() for i in range(doc.page_count)]
    return "\n".join(pages)


def main() -> None:
    if not PDF.exists():
        print(f"Missing PDF: {PDF}")
        return
    doc = fitz.open(str(PDF))
    pages = []
    for i in range(doc.page_count):
        pages.append({"page": i + 1, "text": doc[i].get_text()})
    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
    full = extract_full_text()
    count = len(re.findall(r"(?:^|\n)(\d+)\)\s", full))
    print(f"Wrote {len(pages)} pages -> {OUT_RAW} ({count} question markers found)")


if __name__ == "__main__":
    main()
