"""Extract text from MoEE Model Exam 1 PDF."""

from __future__ import annotations

import json
import re
from pathlib import Path

import fitz

PDF = Path(
    r"c:\Users\Hp\AppData\Roaming\Cursor\User\workspaceStorage"
    r"\87ef23a07efdc78cd48c499e89b4651a\pdfs"
    r"\2cdf9be8-f112-4242-b871-a52c73d1ca8c"
    r"\MODEL1.pdf"
)
OUT_RAW = Path(__file__).resolve().parent.parent / "data" / "exams" / "model1" / "raw_text.json"


def main() -> None:
    if not PDF.exists():
        print(f"Missing PDF: {PDF}")
        return
    doc = fitz.open(str(PDF))
    pages = [{"page": i + 1, "text": doc[i].get_text()} for i in range(doc.page_count)]
    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
    full = "\n".join(p["text"] for p in pages)
    count = len(re.findall(r"(?:^|\n)(\d+)\.\s", full))
    print(f"Wrote {len(pages)} pages -> {OUT_RAW} ({count} question markers)")


if __name__ == "__main__":
    main()
