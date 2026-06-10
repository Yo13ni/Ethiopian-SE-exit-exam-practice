"""Map 2017 screenshot files to exam question numbers via targeted OCR crops."""

from __future__ import annotations

import asyncio
import io
import json
import re
from pathlib import Path

from PIL import Image
from winrt.windows.graphics.imaging import BitmapDecoder
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.storage.streams import DataWriter, InMemoryRandomAccessStream

ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = Path(
    r"C:\Users\Hp\AppData\Roaming\Cursor\User\workspaceStorage"
    r"\d5a59c4bacc7f49b4b12a545283c3af4\images"
)
OUT = ROOT / "data" / "exams" / "2017" / "number_map.json"


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


def crop_png(path: Path, box: tuple[float, float, float, float]) -> bytes:
    img = Image.open(path)
    w, h = img.size
    l, t, r, b = box
    cropped = img.crop((int(w * l), int(h * t), int(w * r), int(h * b)))
    buf = io.BytesIO()
    cropped.save(buf, format="PNG")
    return buf.getvalue()


def extract_number(*texts: str) -> int | None:
    for text in texts:
        for pat in [
            r"(?:Question|Quetion|uestion)\s+(\d{1,3})",
            r"(\d{1,3})\s+out\s+of",
            r"^(\d{1,3})\s+Wh",
        ]:
            m = re.search(pat, text, re.I | re.M)
            if m:
                n = int(m.group(1))
                if 1 <= n <= 100:
                    return n
    return None


def main() -> None:
    files = sorted(IMAGE_DIR.glob("photo_174972*.png"))
    mapping: list[dict] = []
    print(f"Mapping {len(files)} files...", flush=True)

    crops = [
        (0, 0, 0.18, 0.35, "top_left"),
        (0, 0, 0.25, 0.45, "left_panel"),
        (0, 0, 1.0, 1.0, "full"),
    ]

    for i, path in enumerate(files, start=1):
        texts: dict[str, str] = {}
        for l, t, r, b, name in crops:
            try:
                texts[name] = asyncio.run(ocr_png(crop_png(path, (l, t, r, b))))
            except Exception:
                texts[name] = ""

        num = extract_number(texts["top_left"], texts["left_panel"], texts["full"])
        mapping.append({
            "page": i,
            "file": path.name,
            "examNumber": num,
            "ocrHints": {k: v[:80] for k, v in texts.items() if v.strip()},
        })
        if i % 10 == 0:
            print(f"  {i}/{len(files)}", flush=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")
    found = sum(1 for m in mapping if m["examNumber"])
    print(f"Mapped {found}/{len(files)} question numbers -> {OUT}")


if __name__ == "__main__":
    main()
