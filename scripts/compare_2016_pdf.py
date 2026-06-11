"""OCR 2016 reExam PDF and compare with web questions.json."""

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
    r"\60c43bca-91f2-464e-948e-40fbf37f9567\Exit Exam(2016 reExam).pdf"
)
WEB = Path(__file__).resolve().parent.parent / "data" / "exams" / "2016" / "questions.json"
OUT = Path(__file__).resolve().parent.parent / "data" / "exams" / "2016" / "pdf_ocr_text.json"


def ocr_pdf(max_pages: int | None = None) -> list[str]:
    reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    doc = fitz.open(PDF)
    pages: list[str] = []
    n = doc.page_count if max_pages is None else min(max_pages, doc.page_count)
    for i in range(n):
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(2, 2))
        img = pix.tobytes("png")
        lines = reader.readtext(img, detail=0, paragraph=True)
        text = "\n".join(lines)
        pages.append(text)
        print(f"OCR page {i + 1}/{n} ({len(text)} chars)", file=sys.stderr)
    return pages


def normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def stem_words(text: str, n: int = 12) -> set[str]:
    words = [w for w in normalize(text).split() if len(w) > 2]
    return set(words[:n])


def find_best_match(stem: str, ocr_blob: str) -> tuple[float, str]:
    stem_norm = normalize(stem)
    blob_norm = normalize(ocr_blob)
    if stem_norm[:40] and stem_norm[:40] in blob_norm:
        return 1.0, "prefix"
    sw = stem_words(stem)
    if not sw:
        return 0.0, "empty"
    bw = set(blob_norm.split())
    overlap = len(sw & bw) / len(sw)
    return overlap, "words"


def compare(pages: list[str]) -> dict:
    web = json.loads(WEB.read_text(encoding="utf-8"))
    ocr_blob = "\n".join(pages)
    ocr_norm = normalize(ocr_blob)

    results = []
    strong = weak = missing = 0
    for q in web["questions"]:
        num = q["examNumber"]
        stem = q["text"]
        score, method = find_best_match(stem, ocr_blob)
        status = "match" if score >= 0.55 else ("partial" if score >= 0.35 else "missing")
        if status == "match":
            strong += 1
        elif status == "partial":
            weak += 1
        else:
            missing += 1
        results.append({
            "examNumber": num,
            "topic": q.get("topic"),
            "webStem": stem[:120],
            "score": round(score, 2),
            "method": method,
            "status": status,
        })

    # Check for numbered questions in OCR not in web (rough)
    ocr_qnums = set(int(m) for m in re.findall(r"(?<!\d)([1-9]\d?|100)(?=\s*[.)])", ocr_blob))
    return {
        "pdfPages": len(pages),
        "webQuestions": len(web["questions"]),
        "strongMatch": strong,
        "partialMatch": weak,
        "missingInPdf": missing,
        "ocrQuestionNumbersSeen": sorted(ocr_qnums),
        "results": results,
        "ocrSample": ocr_blob[:3000],
    }


def main() -> None:
    max_pages = int(sys.argv[1]) if len(sys.argv) > 1 else None
    pages = ocr_pdf(max_pages)
    OUT.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
    report = compare(pages)
    report_path = OUT.with_name("pdf_compare_report.json")
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: report[k] for k in report if k != "results"}, indent=2))
    print("\nMissing/partial questions:")
    for r in report["results"]:
        if r["status"] != "match":
            print(f"  Q{r['examNumber']} [{r['status']}] score={r['score']} | {r['webStem'][:80]}")


if __name__ == "__main__":
    main()
