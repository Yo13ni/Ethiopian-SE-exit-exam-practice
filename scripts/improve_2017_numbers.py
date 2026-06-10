"""Improve 2017 question number map from OCR hint patterns."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = ROOT / "data" / "exams" / "2017" / "number_map.json"


def extract_from_text(text: str) -> int | None:
    patterns = [
        r"(?:Question|Quetion|Qrstion|uestion|estion)\s+(\d{1,3})",
        r"(?:^|\s)(\d{1,3})\s+out\s+of",
        r"Hide\s+i\s+(\d{1,3})\b",
        r"(?:^|\s)(\d{1,3})\s+(?:yet|ned|Not)\b",
        r"(?:^|\s)(\d{1,3})\s+Which\b",
        r"(?:^|\s)(\d{1,3})\s+What\b",
        r"(?:^|\s)(\d{1,3})\s+Write\b",
        r"(?:^|\s)(\d{1,3})\s+Time\b",
        r"(?:^|\s)(\d{1,3})\s+of\b",
        r"(?:^|\s)(\d{1,3})\s+ed\b",
        r"(?:^|\s)\.(\d{1,3})\s+",
        r"(?:^|\s)n\s+(\d{1,3})\b",
        r"(?:^|\s)on\s+(\d{1,3})\b",
        r"(?:^|\s)tion\s+(\d{1,3})\b",
        r"(?:^|\s)Hic\s+(\d{1,3})\b",
        r"(?:^|\s)Hid\s+(\d{1,3})\b",
        r"(?:^|\s)stim\s+(\d{1,3})\b",
        r"(?:^|\s)MoEEP\s+(\d{1,3})\b",
        r"—\s+(\d{1,3})\s+Which",
        r"(\d{1,3})\s+out\s+cf",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.I)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 100:
                return n
    return None


def main() -> None:
    rows = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    improved = 0
    for row in rows:
        if row.get("examNumber"):
            continue
        blob = " ".join(row.get("ocrHints", {}).values())
        num = extract_from_text(blob)
        if num:
            row["examNumber"] = num
            improved += 1

    MAP_PATH.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    found = sum(1 for r in rows if r.get("examNumber"))
    print(f"Improved {improved} mappings; total mapped {found}/{len(rows)}")


if __name__ == "__main__":
    main()
