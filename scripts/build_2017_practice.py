"""Build 2017 Software Engineering Exit Exam questions.json from OCR."""

from __future__ import annotations

import json
import re
from pathlib import Path

from bdu_answer_solver import solve_answer
from exam2017_data import (
    FOCUS_GUIDE,
    MANUAL_ANSWERS,
    QUESTION_FIXES,
    TOPIC_RULES,
)

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "exams" / "2017" / "raw_ocr.json"
MAP_PATH = ROOT / "data" / "exams" / "2017" / "number_map.json"
MATCHED_PATH = ROOT / "data" / "exams" / "2017" / "matched_answers.json"
CURATED_PATH = ROOT / "data" / "exams" / "2017" / "curated_questions.json"
OUT_PATH = ROOT / "data" / "exams" / "2017" / "questions.json"


def classify(text: str) -> str:
    for topic, pat in TOPIC_RULES:
        if re.search(pat, text, re.I):
            return topic
    return "General"


def normalize_options(opts: list[dict]) -> list[dict]:
    keys = ["A", "B", "C", "D"]
    by = {o["key"]: o["text"] for o in opts if o.get("key") and o.get("text")}
    return [
        {"key": k, "text": (by.get(k) or "(option unclear in OCR)")[:500]}
        for k in keys
    ]


def concept_line(topic: str, answer: str | None, options: list[dict]) -> str:
    if not answer:
        return f"Review this {topic} concept in your notes."
    correct = next((o for o in options if o["key"] == answer), None)
    if correct:
        t = correct["text"]
        return f"Key idea ({topic}): {t[:120]}{'…' if len(t) > 120 else ''}"
    return f"Key idea ({topic}): answer {answer}"


def load_curated() -> dict[int, dict]:
    if not CURATED_PATH.exists():
        return {}
    rows = json.loads(CURATED_PATH.read_text(encoding="utf-8"))
    out: dict[int, dict] = {}
    for row in rows:
        n = row.get("examNumber")
        if n:
            out[int(n)] = row
    return out


def load_number_map() -> dict[int, int]:
    if not MAP_PATH.exists():
        return {}
    rows = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    return {int(r["page"]): int(r["examNumber"]) for r in rows if r.get("examNumber")}


def load_matched() -> dict[int, str]:
    if not MATCHED_PATH.exists():
        return {}
    raw = json.loads(MATCHED_PATH.read_text(encoding="utf-8"))
    return {int(k): v for k, v in raw.items()}


def collect_by_exam_number(pages: list[dict]) -> dict[int, dict]:
    by_num: dict[int, dict] = {}
    for page in pages:
        parsed = page.get("parsed", {})
        exam_num = parsed.get("examNumber")
        if not exam_num:
            continue
        text = parsed.get("text", "")
        opts = parsed.get("options", [])
        if len(text) < 8 and len(opts) < 2:
            continue
        prev = by_num.get(exam_num)
        score = len(text) + sum(len(o.get("text", "")) for o in opts)
        prev_score = 0
        if prev:
            prev_score = len(prev.get("text", "")) + sum(
                len(o.get("text", "")) for o in prev.get("options", [])
            )
        if not prev or score > prev_score:
            by_num[exam_num] = parsed
    return by_num


def resolve_answer(
    exam_num: int,
    text: str,
    options: list[dict],
    matched: dict[int, str],
    topic: str,
) -> str | None:
    fix = QUESTION_FIXES.get(exam_num, {})
    if fix.get("answer"):
        return fix["answer"]
    if exam_num in MANUAL_ANSWERS:
        return MANUAL_ANSWERS[exam_num]
    if exam_num in matched:
        return matched[exam_num]
    return solve_answer(exam_num, text, options, topic)


def build_questions() -> tuple[list[dict], list[str]]:
    if not RAW_PATH.exists():
        raise SystemExit(f"Missing {RAW_PATH}. Run: python scripts/extract_2017_ocr.py")

    pages = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    num_map = load_number_map()
    matched = load_matched()
    curated = load_curated()

    # Apply page→question overrides and improved parser to stored OCR
    from exam2017_parser import parse_2017_page  # noqa: WPS433

    for page in pages:
        raw = page.get("raw", "")
        parsed = parse_2017_page(raw, page.get("page", 0))
        mapped = num_map.get(page.get("page"))
        if mapped:
            parsed["examNumber"] = mapped
        page["parsed"] = parsed

    by_num = collect_by_exam_number(pages)

    # Curated vision transcriptions override OCR
    for exam_num, row in curated.items():
        by_num[exam_num] = {
            "examNumber": exam_num,
            "text": row["text"],
            "options": row["options"],
        }

    # Manual fixes override everything
    for exam_num, fix in QUESTION_FIXES.items():
        by_num[exam_num] = {
            "examNumber": exam_num,
            "text": fix["text"],
            "options": fix["options"],
        }

    questions: list[dict] = []
    skipped: list[str] = []
    seq_id = 0

    for exam_num in sorted(by_num):
        if exam_num > 100:
            skipped.append(f"Q{exam_num}: beyond question 100")
            continue

        parsed = by_num[exam_num]
        fix = QUESTION_FIXES.get(exam_num, {})
        cur = curated.get(exam_num, {})

        text = fix.get("text") or cur.get("text") or parsed.get("text", "").strip()
        options = (
            fix.get("options")
            or cur.get("options")
            or normalize_options(parsed.get("options", []))
        )

        if len(text) < 12:
            skipped.append(f"Q{exam_num}: stem too short")
            continue
        clear_opts = sum(1 for o in options if "(option unclear" not in o["text"])
        if clear_opts < 2 and exam_num not in QUESTION_FIXES:
            skipped.append(f"Q{exam_num}: fewer than 2 parseable options")
            continue

        topic = fix.get("topic") or cur.get("topic") or classify(
            text + " " + " ".join(o["text"] for o in options)
        )
        answer = (
            fix.get("answer")
            or cur.get("answer")
            or resolve_answer(exam_num, text, options, matched, topic)
        )
        if not answer:
            skipped.append(f"Q{exam_num}: missing answer key")
            continue

        seq_id += 1
        questions.append({
            "examNumber": exam_num,
            "id": seq_id,
            "topic": topic,
            "text": text,
            "options": options,
            "answer": answer,
            "concept": concept_line(topic, answer, options),
        })

    return questions, skipped


def main() -> None:
    questions, skipped = build_questions()
    payload = {
        "title": "2017 Software Engineering Exit Exam",
        "source": "2017 Ethiopian University Exit Exam for Software Engineering (MoEE) — Moodle OCR",
        "total": len(questions),
        "timeLimitHours": 3,
        "focusGuide": FOCUS_GUIDE,
        "questions": questions,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(questions)} questions -> {OUT_PATH}")
    nums = {q["examNumber"] for q in questions}
    missing = [n for n in range(1, 101) if n not in nums]
    if missing:
        print(f"Missing exam numbers ({len(missing)}): {missing[:20]}{'...' if len(missing) > 20 else ''}")
    if skipped:
        print(f"Skipped {len(skipped)}:")
        for s in skipped[:15]:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
