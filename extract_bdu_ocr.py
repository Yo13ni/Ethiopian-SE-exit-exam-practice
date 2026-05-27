"""OCR all pages from BDU Model Exit Exam PDF."""

import asyncio
import io
import json
import re
from pathlib import Path

import fitz
from PIL import Image
from winrt.windows.graphics.imaging import BitmapDecoder
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.storage.streams import DataWriter, InMemoryRandomAccessStream

PDF = Path(
    r"c:\Users\Hp\AppData\Roaming\Cursor\User\workspaceStorage"
    r"\87ef23a07efdc78cd48c499e89b4651a\pdfs"
    r"\dc541116-4568-4fcd-bc4e-691b054f77b3"
    r"\Bahir Dar University (BDU) Model Exit Exam.pdf"
)
OUT_RAW = Path(__file__).parent / "data" / "exams" / "bdu" / "raw_ocr.json"
DPI = 200
MAX_QUESTION_PAGE = 99

NOISE = re.compile(
    r"(?i)(model exit exam|microsoft edge|lms\.?bdu|quiz navigation|"
    r"answer saved|marked out of|flag question|select one:?|"
    r"previous page|next page|type here to search|screenshots|"
    r"ee\s*15\s*soft\s*eng|dejen\s*aschalew|dejenaschalew|"
    r"what is websitm|psiphon|mymodelexa|t\.me/dagmawi|"
    r"^\s*o\s*$|profile\s*1|https?://|mod/quiz|attempt\.php|"
    r"\b\d{1,2}\s+\d{2}\s+\d{2}\s+\d{2}\b|1024\s*am|"
    r"channel.*comp sci|youtube|linkedin|instagram|tiktok|github|snapchat)"
)


async def ocr_png(png: bytes) -> str:
    stream = InMemoryRandomAccessStream()
    w = DataWriter(stream)
    w.write_bytes(bytearray(png))
    await w.store_async()
    await w.flush_async()
    w.detach_stream()
    stream.seek(0)
    dec = await BitmapDecoder.create_async(stream)
    bmp = await dec.get_software_bitmap_async()
    eng = OcrEngine.try_create_from_user_profile_languages()
    return (await eng.recognize_async(bmp)).text or ""


def render(doc, i: int) -> bytes:
    page = doc[i]
    pix = page.get_pixmap(matrix=fitz.Matrix(DPI / 72, DPI / 72), alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def clean(text: str) -> str:
    text = NOISE.sub(" ", text)
    text = re.sub(r"\bO\b(?=\s|$)", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_page(raw: str, page_num: int) -> dict:
    num_m = re.search(r"Question\s+(\d+)", raw, re.I)
    qnum = int(num_m.group(1)) if num_m else page_num

    body = clean(raw)

    opts: list[dict] = []
    for m in re.finditer(
        r"(?:^|\s)(?:O\s+)?([A-Da-d])[\.\)]\s*([^A-Da-d]+?)(?=\s(?:O\s+)?[A-Da-d][\.\)]|\s*$)",
        body,
    ):
        opts.append({"key": m.group(1).upper(), "text": m.group(2).strip()})

    if len(opts) < 2:
        parts = re.split(r"\s+(?=(?:O\s+)?[A-Da-d][\.\)]\s)", body, flags=re.I)
        for p in parts[1:]:
            om = re.match(r"^(?:O\s+)?([A-Da-d])[\.\)]\s*(.+)$", p.strip(), re.I | re.S)
            if om:
                opts.append({"key": om.group(1).upper(), "text": om.group(2).strip()})

    first_opt = re.search(r"\s(?:O\s+)?[A-Da-d][\.\)]\s", body, re.I)
    stem = body[: first_opt.start()].strip() if first_opt else body
    stem = re.sub(r"^Question\s+\d+\s*", "", stem, flags=re.I).strip()
    stem = re.sub(r"\s+(?:O\s+)?[A-Da-d][\.\)].*", "", stem, flags=re.I | re.S).strip()

    by_key: dict[str, str] = {}
    for o in opts:
        k, t = o["key"], o["text"]
        if k not in by_key or len(t) > len(by_key[k]):
            by_key[k] = t

    return {
        "page": page_num,
        "examNumber": qnum,
        "raw": raw.strip(),
        "text": stem,
        "options": [{"key": k, "text": by_key[k]} for k in sorted(by_key)][:4],
    }


def is_promo_page(raw: str) -> bool:
    low = raw.lower()
    return "in this channel" in low or ("youtube" in low and "dagmawi" in low)


def main() -> None:
    doc = fitz.open(str(PDF))
    total = doc.page_count
    pages = []
    print(f"OCR {total} pages from BDU PDF...", flush=True)

    for i in range(total):
        pnum = i + 1
        print(f"  {pnum}/{total}", flush=True)
        if pnum > MAX_QUESTION_PAGE and pnum == total:
            pages.append({"page": pnum, "raw": "", "parsed": {"page": pnum, "examNumber": pnum, "text": "", "options": []}, "promo": True})
            continue
        try:
            raw = asyncio.run(ocr_png(render(doc, i)))
        except Exception as e:
            raw = ""
            print(f"    error: {e}", flush=True)
        parsed = parse_page(raw, pnum)
        pages.append({"page": pnum, "raw": raw, "parsed": parsed, "promo": is_promo_page(raw)})

    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
    valid = sum(
        1
        for p in pages
        if not p.get("promo")
        and len(p["parsed"].get("text", "")) > 15
        and len(p["parsed"].get("options", [])) >= 2
    )
    print(f"Done: {valid} parseable questions -> {OUT_RAW}")


if __name__ == "__main__":
    main()
