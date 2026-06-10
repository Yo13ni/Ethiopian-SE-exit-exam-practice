"""OCR 2017 MoEE exit exam screenshots (Moodle UI)."""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path

from winrt.windows.graphics.imaging import BitmapDecoder
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.storage.streams import DataWriter, InMemoryRandomAccessStream

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
import sys

sys.path.insert(0, str(SCRIPTS))
from exam2017_parser import parse_2017_page  # noqa: E402

IMAGE_DIRS = [
    ROOT / "data" / "exams" / "2017" / "images",
    Path(
        r"C:\Users\Hp\AppData\Roaming\Cursor\User\workspaceStorage"
        r"\d5a59c4bacc7f49b4b12a545283c3af4\images"
    ),
]

OUT_RAW = ROOT / "data" / "exams" / "2017" / "raw_ocr.json"

async def ocr_file(path: Path) -> str:
    data = path.read_bytes()
    stream = InMemoryRandomAccessStream()
    w = DataWriter(stream)
    w.write_bytes(bytearray(data))
    await w.store_async()
    await w.flush_async()
    w.detach_stream()
    stream.seek(0)
    dec = await BitmapDecoder.create_async(stream)
    bmp = await dec.get_software_bitmap_async()
    eng = OcrEngine.try_create_from_user_profile_languages()
    return (await eng.recognize_async(bmp)).text or ""


def find_images() -> list[Path]:
    for d in IMAGE_DIRS:
        if not d.is_dir():
            continue
        files = sorted(d.glob("photo_174972*.png"))
        if files:
            print(f"Using {len(files)} images from {d}")
            return files
    raise SystemExit("No photo_174972*.png images found. Copy screenshots to data/exams/2017/images/")


def main() -> None:
    images = find_images()
    pages = []
    print(f"OCR {len(images)} images...", flush=True)

    for i, path in enumerate(images, start=1):
        print(f"  {i}/{len(images)} {path.name[:40]}...", flush=True)
        try:
            raw = asyncio.run(ocr_file(path))
        except Exception as e:
            raw = ""
            print(f"    error: {e}", flush=True)
        parsed = parse_2017_page(raw, i)
        pages.append({
            "page": i,
            "file": path.name,
            "raw": raw,
            "parsed": parsed,
        })

    OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUT_RAW.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")

    by_num: dict[int, dict] = {}
    for p in pages:
        n = p["parsed"]["examNumber"]
        if len(p["parsed"].get("text", "")) > 10 and len(p["parsed"].get("options", [])) >= 2:
            prev = by_num.get(n)
            if not prev or len(p["parsed"]["text"]) > len(prev["parsed"]["text"]):
                by_num[n] = p

    print(f"Done: {len(by_num)} unique questions (by exam number) -> {OUT_RAW}")


if __name__ == "__main__":
    main()
