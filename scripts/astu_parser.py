"""Parse ASTU Software Engineering MCQ PDF text into questions."""

from __future__ import annotations

import re


def clean_intro(text: str) -> str:
    text = re.sub(r"\d+\s*\|\s*P\s*a\s*g\s*e\s*", "", text)
    text = re.sub(
        r"Software Engineering MCQs[\s\S]*?various options\.\s*",
        "",
        text,
        count=1,
        flags=re.I,
    )
    return text


def parse_options(body: str) -> tuple[str, list[dict]]:
    body = re.sub(r"Show Answer Workspace\s*", "", body, flags=re.I)
    first = re.search(r"(?:^|\n)([a-d])\.\s", body, re.I)
    if not first:
        return re.sub(r"\s+", " ", body).strip(), []

    stem = body[: first.start()].strip()
    stem = re.sub(r"\s+", " ", stem).strip()

    opts: list[dict] = []
    for m in re.finditer(
        r"(?:^|\n)([a-d])\.\s*\n?\s*(.+?)(?=(?:\n[a-d]\.\s)|$)",
        body,
        re.I | re.S,
    ):
        text = re.sub(r"\s+", " ", m.group(2)).strip()
        text = re.sub(r"^[dD]\)\s*", "", text)
        if text:
            opts.append({"key": m.group(1).upper(), "text": text[:500]})

    by_key: dict[str, str] = {}
    for o in opts:
        k, t = o["key"], o["text"]
        if k not in by_key or len(t) > len(by_key[k]):
            by_key[k] = t

    ordered = [{"key": k, "text": by_key[k]} for k in "ABCD" if k in by_key]
    return stem, ordered[:4]


def parse_all_questions(full_text: str) -> list[dict]:
    text = clean_intro(full_text)
    parts = re.split(r"(?=(?:^|\n)\d+\)\s)", text, flags=re.M)
    questions: list[dict] = []

    for part in parts:
        m = re.match(r"(\d+)\)\s*(.+)", part.strip(), re.S)
        if not m:
            continue
        num = int(m.group(1))
        if num < 1 or num > 60:
            continue
        stem, options = parse_options(m.group(2))
        if len(stem) < 8 or len(options) < 2:
            continue
        questions.append({"examNumber": num, "text": stem, "options": options})

    by_num = {q["examNumber"]: q for q in questions}
    return [by_num[n] for n in sorted(by_num) if 1 <= n <= 60]
