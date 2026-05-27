"""OCR all pages from AAU Model Exit Exam PDF."""

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
    r"\9a88ab94-c0d6-4e65-949f-36bfef41c136"
    r"\Addis Ababa Univeristy (AAU) Model Exit Exam.pdf"
)
OUT_RAW = Path(r"c:\Users\Hp\project\research\practice-app\data\exams\aau\raw_ocr.json")
DPI = 200

NOISE = re.compile(
    r"(?i)(not\s+yet\s+answered|marked\s+out\s+of|flag\s+question|select\s+one:?|"
    r"quiz\s+navigation|aa?it\s+learning|management\s+system|t\.me/dagmawi|"
    r"^\s*next\s*$|^\s*o\s*$|aaaaaa|oaoooo|question\s+\d+\s*$)"
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


def render(doc, i):
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
    text = re.sub(r"^Question\s+\d+\s*", "", text, flags=re.I)
    return text


def parse_page(raw: str, page_num: int) -> dict:
    num_m = re.search(r"Question\s+(\d+)", raw, re.I)
    qnum = int(num_m.group(1)) if num_m else page_num

    body = clean(raw)

    # Extract labeled options: a. b. c. d. or O a. patterns
    opts = []
    for m in re.finditer(
        r"(?:^|\s)([a-d])\.\s*([^a-d]+?)(?=\s[a-d]\.\s|$)",
        body,
        re.I,
    ):
        opts.append({"key": m.group(1).upper(), "text": m.group(2).strip()})

    if len(opts) < 2:
        # fallback split on a. b. c. d.
        parts = re.split(r"\s+(?=[a-d]\.\s)", body, flags=re.I)
        stem = parts[0]
        for p in parts[1:]:
            om = re.match(r"^([a-d])\.\s*(.+)$", p.strip(), re.I)
            if om:
                opts.append({"key": om.group(1).upper(), "text": om.group(2).strip()})
    else:
        first_opt = re.search(r"\s[a-d]\.\s", body, re.I)
        stem = body[: first_opt.start()].strip() if first_opt else body

    stem = re.sub(r"\s+[a-d]\.\s.*", "", stem, flags=re.I | re.S).strip()
    stem = re.sub(r"\s+", " ", stem)

    return {
        "page": page_num,
        "examNumber": qnum,
        "raw": raw.strip(),
        "text": stem,
        "options": opts[:4],
    }


def main():
    doc = fitz.open(str(PDF))
    total = doc.page_count
    pages = []
    print(f"OCR {total} pages from AAU PDF...", flush=True)

    for i in range(total):
        print(f"  {i + 1}/{total}", flush=True)
        try:
            raw = asyncio.run(ocr_png(render(doc, i)))
        except Exception as e:
            raw = ""
            print(f"    error: {e}", flush=True)
        pages.append({"page": i + 1, "raw": raw, "parsed": parse_page(raw, i + 1)})

    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
    valid = sum(1 for p in pages if len(p["parsed"]["text"]) > 20 and len(p["parsed"]["options"]) >= 2)
    print(f"Done: {valid} parseable questions -> {OUT_RAW}")


if __name__ == "__main__":
    main()
