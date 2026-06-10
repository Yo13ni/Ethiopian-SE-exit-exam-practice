"""Parse BDU Moodle screenshot OCR into clean question stems and options."""

from __future__ import annotations

import re


NOISE_PATTERNS = [
    r"model exit exam",
    r"\(new \(page \d+ of \d+\)",
    r"microsoft edge",
    r"profile \d+",
    r"lms\.?bdu\.?edu\.?et",
    r"mod/quiz/attempt\.php[^\s]*",
    r"quiz navigation",
    r"answer saved",
    r"not yet answered",
    r"marked out of",
    r"flag question",
    r"select one:?",
    r"previous page",
    r"next page",
    r"type here to search",
    r"ee\s*15\s*soft\s*eng",
    r"dejen\s*aschalew",
    r"dejenaschalew",
    r"t\.me/dagmawi[^\s]*",
    r"what is websitm",
    r"what is website",
    r"psiphon",
    r"screenshots",
    r"mymodelexam",
    r"model exit exm",
    r"https?://[^\s]+",
    r"\b\d{1,2}\s+\d{2}\s+\d{2}\s+\d{2}\b",
    r"\b102[45]\s*am\b",
    r"^\s*question\s+i\s*$",
    r"^\s*question\s*$",
    r"^\s*o\s*$",
    r"^\s*p\s*$",
    r"^\s*it\s*$",
    r"^\s*-\s*$",
    r"\.edu\.et",
    r"\?attempt",
    r"\?attem",
    r"cmid=\d+",
    r"page=\d+",
    r"pt=\d+",
]

_NOISE = [re.compile(p, re.I) for p in NOISE_PATTERNS]

# Trim option text at these markers
_OPTION_TAIL = re.compile(
    r"(?i)\b(previous page|next page|model exit|quiz navigation|https?:|screenshots|psiphon|mymodel|\d{3,4}\s*am)\b.*",
    re.S,
)


def clean_text(text: str) -> str:
    for pat in _NOISE:
        text = pat.sub(" ", text)
    text = re.sub(r"\bO\b(?=\s|$)", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^[\(\)\-\.\s]+", "", text).strip()
    return text


def extract_stem(raw: str) -> str:
    text = raw
    # Prefer content after student/course banner
    m = re.search(
        r"(?:Dejen\s*Aschalew|SOFT\s*ENG)\s*(.+?)(?:Select one:|PREVIOUS PAGE|$)",
        text,
        re.I | re.S,
    )
    if m:
        stem = m.group(1)
    else:
        m2 = re.search(
            r"Question\s+(?:\d+|I)\s*(?:Answer saved|Not yet answered|Marked out of)?\s*(?:Flag question)?\s*(.+?)(?:Select one:|PREVIOUS PAGE|$)",
            text,
            re.I | re.S,
        )
        stem = m2.group(1) if m2 else text

    stem = _OPTION_TAIL.sub("", stem)
    stem = clean_text(stem)
    stem = re.sub(r"^Question\s+\d+\s*", "", stem, flags=re.I)
    stem = re.sub(r"\s+(?:Select one|o\s*)$", "", stem, flags=re.I)
    return stem.strip(" ?.")


def parse_options(raw: str) -> list[dict]:
    # Isolate option block after "Select one"
    block = raw
    sel = re.search(r"Select one:\s*(.+?)(?:PREVIOUS PAGE|NEXT PAGE|Quiz navigation|$)", raw, re.I | re.S)
    if sel:
        block = sel.group(1)

    block = _OPTION_TAIL.sub("", block)

    # Split on a. b. c. d. or A. B. etc (comma after c is OCR artifact)
    parts = re.split(r"(?<=\s)([A-Da-d])[\.,]\s+", block)
    if len(parts) <= 1:
        parts = re.split(r"(?<=\s)([A-Da-d])[\.,]\s+", " " + block)

    opts: list[dict] = []
    if len(parts) > 1:
        # parts[0] is junk before first option
        for i in range(1, len(parts), 2):
            if i + 1 >= len(parts):
                break
            key = parts[i].upper()
            text = clean_text(parts[i + 1])
            text = re.split(r"\s+[cC][\.,]\s+", text)[0]  # drop merged next option
            if text and len(text) > 1:
                opts.append({"key": key, "text": text[:400]})

    # Deduplicate by key, keep longest clean text
    by_key: dict[str, str] = {}
    for o in opts:
        k, t = o["key"], o["text"]
        if k not in by_key or len(t) > len(by_key[k]):
            by_key[k] = t

    keys = ["A", "B", "C", "D"]
    return [{"key": k, "text": by_key.get(k, "(option unclear in OCR)")} for k in keys if k in by_key or by_key]


def normalize_four(options: list[dict]) -> list[dict]:
    keys = ["A", "B", "C", "D"]
    by = {o["key"]: o["text"] for o in options}
    return [{"key": k, "text": (by.get(k) or "(option unclear in OCR)")[:500]} for k in keys]


def parse_bdu_page(raw: str, page_num: int) -> dict:
    stem = extract_stem(raw)
    options = normalize_four(parse_options(raw))
    return {
        "page": page_num,
        "examNumber": page_num,
        "text": stem,
        "options": options,
    }


def is_promo(raw: str) -> bool:
    low = raw.lower()
    return "in this channel" in low and "youtube" in low
