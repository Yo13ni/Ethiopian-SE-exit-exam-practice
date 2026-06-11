#!/usr/bin/env python3
"""Copy data/ into public/data/ for static hosting on Vercel."""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data"
DEST = ROOT / "public" / "data"


def main() -> None:
    if not SRC.is_dir():
        raise SystemExit(f"Missing data directory: {SRC}")
    if DEST.exists():
        shutil.rmtree(DEST)
    shutil.copytree(SRC, DEST)
    print(f"Copied {SRC} -> {DEST}")


if __name__ == "__main__":
    main()
