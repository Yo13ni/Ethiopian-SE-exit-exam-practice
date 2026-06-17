"""Parse 2017 Moodle screenshot OCR into question stems and options."""

from __future__ import annotations

import re

NOISE_PATTERNS = [
    r"back\b",
    r"not yet answered",
    r"not yet",
    r"marked out of",
    r"matted out of",
    r"maned out of",
    r"marted out of",
    r"ma[åa]?\.?ed out of",
    r"flag question",
    r"flag quest'?on",
    r"previous page",
    r"next page",
    r"next pag\b",
    r"finish attempt",
    r"time left",
    r"exam navigation",
    r"quiz navigation",
    r"hide\b",
    r"select one:?",
    r"^\s*o\s*$",
    r"moeep",
    r"mod/quiz",
    r"question yet\b",
    r"revtous page",
]

_NOISE = [re.compile(p, re.I) for p in NOISE_PATTERNS]

FOOTER = re.compile(
    r"(?i)\b(previous page|next page|next pag|finish attempt|hide|time left|exam navigation|quiz navigation)\b.*"
)

# Moodle exam-navigation grid at bottom/right (e.g. "1 10 19 28 37 46 55")
NAV_GRID = re.compile(
    r"(?:\b(?:next page|hide)\b\s*)?"
    r"(?:\b\d{1,2}\s+){2,}\d{1,2}\s*$",
    re.I,
)

# Timer remnant after "time left" is stripped (e.g. "2:54:28 ot Scheduling...")
TIMER_REMNANT = re.compile(r"^\d{1,2}:\d{2}:\d{2}\s*(?:ot\s+)?", re.I)

QUESTION_NUM = re.compile(
    r"(?i)\b(?:back\s+)?question\s+(\d{1,3})\b"
    r"(?:\s+(?:not\s+yet|answer\s+saved|marked|matted|maned|flag))?",
)


def clean_text(text: str) -> str:
    text = NAV_GRID.sub("", text)
    for pat in _NOISE:
        text = pat.sub(" ", text)
    text = re.sub(r"\bO\b(?=\s|$)", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def strip_sidebar(raw: str) -> str:
    """Remove Moodle chrome before parsing stem/options."""
    text = raw
    # Drop right-side exam navigation block when OCR merges it into one line.
    text = NAV_GRID.sub("", text)
    text = re.sub(
        r"(?i)\b(?:exam|quiz)\s+navigation\b.*$",
        "",
        text,
    )
    return text.strip()


def extract_exam_number(raw: str, file_index: int) -> int:
    # Left sidebar "Question 73" is authoritative — never use page/file index or nav grid.
    for m in QUESTION_NUM.finditer(raw):
        n = int(m.group(1))
        if 1 <= n <= 100:
            return n

    for pat in [
        r"Quetion\s+(\d{1,3})",
        r"(?:^|\s)(\d{1,3})\s+out\s+of\s+(?:1\.00|1,00|\d)",
        r"Hide\s+i\s+(\d{1,3})\b",
        r"\bi\s+(\d{1,3})\s+xxs\b",
    ]:
        m = re.search(pat, raw, re.I)
        if m:
            n = int(m.group(1))
            if 1 <= n <= 100:
                return n

    # Standalone leading number before stem (e.g. "26 Which software...")
    m = re.match(r"^\s*(\d{1,3})\s+(?=[A-Z])", raw.strip())
    if m:
        n = int(m.group(1))
        if 1 <= n <= 100:
            return n

    return file_index


def _parse_abcd(body: str) -> list[dict]:
    opts: list[dict] = []
    for m in re.finditer(
        r"(?:^|\s)(?:O\s+)?([A-Da-d])[\.\)]\s*([^A-Da-d]+?)(?=\s(?:O\s+)?[A-Da-d][\.\)]|\s*$)",
        body,
    ):
        opts.append({"key": m.group(1).upper(), "text": m.group(2).strip()})

    if len(opts) < 2:
        # "a. b. c. d. text text text" — labels clustered, text follows
        m = re.search(
            r"(?:O\s+)?[A-Da-d][\.\)]\s*(?:O\s+)?[A-Da-d][\.\)]\s*(?:O\s+)?[A-Da-d][\.\)]\s*(?:O\s+)?[A-Da-d][\.\)]\s*(.+)$",
            body,
            re.I | re.S,
        )
        if m:
            blob = m.group(1).strip()
            parts = _split_four(blob)
            if len(parts) == 4:
                return [{"key": k, "text": t} for k, t in zip("ABCD", parts)]

    by_key: dict[str, str] = {}
    for o in opts:
        k, t = o["key"], o["text"]
        if k not in by_key or len(t) > len(by_key[k]):
            by_key[k] = t
    return [{"key": k, "text": by_key[k]} for k in sorted(by_key)][:4]


def _merge_to_four(parts: list[str]) -> list[str]:
    parts = [p.strip().rstrip(".") for p in parts if p.strip()]
    while len(parts) > 4:
        best_i, best_len = 0, float("inf")
        for i in range(len(parts) - 1):
            combined = len(parts[i]) + len(parts[i + 1])
            if combined < best_len:
                best_len = combined
                best_i = i
        parts[best_i : best_i + 2] = [f"{parts[best_i]} {parts[best_i + 1]}".strip()]
    return parts if len(parts) == 4 else []


def _split_four(blob: str) -> list[str]:
    blob = FOOTER.sub("", blob).strip()
    if not blob:
        return []

    strategies: list[list[str]] = []

    if ": " in blob and blob.count(". ") >= 3:
        colon_parts = re.split(r"(?<=\.)\s+(?=[A-Z])", blob)
        colon_parts = [p.strip().rstrip(".") for p in colon_parts if len(p.strip()) > 5]
        merged_colon = _merge_to_four(colon_parts)
        if merged_colon:
            strategies.append(merged_colon)

    if blob.count("To ") >= 4:
        parts = [p.strip().rstrip(".") for p in re.split(r"(?=To )", blob) if p.strip()]
        if len(parts) >= 4:
            strategies.append(parts[:4])

    if ";" in blob:
        parts = [p.strip().rstrip(":") for p in blob.split(";") if len(p.strip()) > 3]
        if len(parts) >= 4:
            strategies.append(parts[:4])

    cap_parts = re.split(r"(?<=[a-z\)])(?=\s+[A-Z])", blob)
    cap_parts = [p.strip().rstrip(".") for p in cap_parts if len(p.strip()) > 1]
    merged = _merge_to_four(cap_parts)
    if merged:
        strategies.append(merged)

    sort_parts = re.split(r"(?<=\bSort)(?=\s+[A-Z])", blob)
    sort_parts = [p.strip() for p in sort_parts if p.strip()]
    if len(sort_parts) >= 4:
        strategies.append(sort_parts[:4])

    # ML / maintenance style: split before known option-leading words
    kw_parts = re.split(
        r"(?=\s*(?:Adaptive|Corrective|Perfective|Preventive|Encapsulation|Access method|"
        r"Flow control|Response timeout|Clustering|Regression|Classification|Merge|Bubble|"
        r"Selection|Insertion|REST|WebSocket|GraphQL|HTTP)\b)",
        blob,
        flags=re.I,
    )
    kw_parts = [p.strip().rstrip(".") for p in kw_parts if len(p.strip()) > 2]
    merged_kw = _merge_to_four(kw_parts)
    if merged_kw:
        strategies.append(merged_kw)

    if len(strategies) == 1:
        return strategies[0]

    if strategies:
        def score(parts: list[str]) -> float:
            if len(parts) != 4:
                return -1
            lens = [len(p) for p in parts]
            if min(lens) < 3:
                return -1
            return 100 - (max(lens) - min(lens))

        return max(strategies, key=score)

    return []


def _option_blob(body: str) -> str:
    qm = list(re.finditer(r"\?", body))
    if qm:
        return body[qm[-1].end() :].strip()
    colon = re.search(r":\s*(?:[A-Z]|Rely|Delegate|Provide|Distribute|To )", body)
    if colon:
        return body[colon.end() - 1 :].strip().lstrip(": ")
    # No question mark — take text after last period before footer-like noise
    m = re.search(
        r"(?:problem|following|below|true|correct|best suited|used for|refers to|purpose of|goal of)"
        r"[^.?!]*[.?!]\s*(.+)$",
        body,
        re.I | re.S,
    )
    if m:
        return m.group(1).strip()
    return ""


def parse_options(body: str) -> list[dict]:
    abcd = _parse_abcd(body)
    if len(abcd) >= 2 and all(len(o["text"]) > 2 for o in abcd):
        if len(abcd) == 4:
            return abcd
        parts = _split_four(" ".join(o["text"] for o in abcd))
        if len(parts) == 4:
            return [{"key": k, "text": t} for k, t in zip("ABCD", parts)]

    opt_blob = _option_blob(body)
    opt_blob = FOOTER.sub("", opt_blob).strip()
    parts = _split_four(opt_blob)
    if len(parts) == 4:
        return [{"key": k, "text": t} for k, t in zip("ABCD", parts)]
    return []


def extract_stem(body: str, options: list[dict]) -> str:
    body = FOOTER.sub("", body)
    qm = list(re.finditer(r"\?", body))
    if qm:
        stem = body[: qm[-1].end()].strip()
    else:
        first_abcd = re.search(r"\s(?:O\s+)?[A-Da-d][\.\)]\s", body, re.I)
        if first_abcd:
            stem = body[: first_abcd.start()].strip()
        elif options:
            # Remove trailing option text from body
            stem = body
            for o in reversed(options):
                idx = stem.rfind(o["text"])
                if idx > 20:
                    stem = stem[:idx].strip()
        else:
            stem = body

    stem = clean_text(stem)
    stem = re.sub(r"^Question\s+\d+\s*", "", stem, flags=re.I)
    stem = re.sub(r"^Quetion\s+\d+\s*", "", stem, flags=re.I)
    stem = re.sub(r"^\d{1,3}\s+(?:yet|ned)\s+\w*\s*", "", stem, flags=re.I)
    stem = re.sub(r"^\d{1,3}\s+out\s+of\s+[^?]*", "", stem, flags=re.I)
    stem = re.sub(r"^[A-Za-z]+\s+out\s+of\s+[^?]*", "", stem, flags=re.I)
    stem = TIMER_REMNANT.sub("", stem)
    stem = re.sub(r"^(?:ot|hide|hic)\s+", "", stem, flags=re.I)
    stem = re.sub(r"^\d{1,3}\s+(?=\d{1,2}:\d{2})[^?]*", "", stem)
    return stem.strip()


def parse_2017_page(raw: str, file_index: int) -> dict:
    exam_number = extract_exam_number(raw, file_index)
    body = clean_text(strip_sidebar(raw))
    options = parse_options(body)
    text = extract_stem(body, options)

    by_key: dict[str, str] = {}
    for o in options:
        k, t = o["key"], clean_text(o["text"])
        if k not in by_key or len(t) > len(by_key[k]):
            by_key[k] = t

    norm_opts = [{"key": k, "text": by_key[k]} for k in sorted(by_key)][:4]

    return {
        "fileIndex": file_index,
        "examNumber": exam_number,
        "raw": raw.strip(),
        "text": text,
        "options": norm_opts,
    }
