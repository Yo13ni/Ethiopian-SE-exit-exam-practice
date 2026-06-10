"""Build AAU Model Exit Exam practice questions.json from OCR pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

from aau_exam_data import ANSWERS, FOCUS_GUIDE, MANUAL_OVERRIDES

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "exams" / "aau" / "raw_ocr.json"
OUT_PATH = ROOT / "data" / "exams" / "aau" / "questions.json"

NOISE_PATTERNS = [
    r"not\s+yet\s+answered",
    r"marked\s+(?:out|aut)\s+of",
    r"flag\s+quest(?:ion|idn)",
    r"select\s+one:?",
    r"quiz\s+navigation",
    r"aa?it\s+question\s+\d*",
    r"aa?it\s+learning",
    r"managern?ent\s+syste?rn?a?",
    r"t\.me/dagmawi[_\w]*",
    r"^\s*next\s*$",
    r"^\s*o\s*$",
    r"\ba{4,}\b",
    r"\bo{4,}\b",
    r"^\s*question\s+\d+\s*",
    r"\d{1,2}\s+\d{2}\s+\d{2}\s+\d{2}",  # quiz nav number grids
    r"1\.00",
    r"•e",
    r"westion",
    r"answered\s+d\s+aut",
    r"ig\s+question",
]

_NOISE_COMPILED = [re.compile(p, re.I) for p in NOISE_PATTERNS]

TOPIC_RULES: list[tuple[str, str]] = [
    ("Database", r"relation|functional dependency|foreign key|ER diagram|SQL|entity|attribute|null|cardinality|normal"),
    ("Java/OOP", r"java|polymorph|interface|package scope|exception|garbage|pointer|checked"),
    ("Networking", r"OSI|TCP|ICMP|layer|port|IPv4|wireless|topology|star|bus|mesh|ring|CORS|REST"),
    ("Android", r"android|activity|service|content provider|src folder|lifecycle|onCreate|onClick"),
    ("Security", r"security|cyber|risk|obscurity|digital signature|digest|worm|virus|triple des|public key|economy of"),
    ("PM", r"spiral|critical path|communication management|analogy|scrum|incremental|agile|waterfall|task|milestone"),
    ("AI/ML", r"supervised|search algorithm|BFS|DFS|UCS|Dijkstra|A\*|uninformed|informed|local search|heuristic"),
    ("SE", r"SRS|requirement|testing|maintenance|regression|architecture|coupling|quality scenario"),
    ("OS", r"operating system|process|thread|fork|READY|memory management|swapping|paging|program counter"),
    ("C++", r"C\+\+|cout|void solve|time complexity"),
    ("Web", r"CSS|javascript|HTTP|spread|getElement|async"),
    ("Data Structures", r"queue|stack|sort|selection sort|binary search|swap|data structure"),
    ("Software Architecture", r"layered architecture|software architecture|quality attribute|stakeholder"),
]


def clean_text(text: str) -> str:
    for pat in _NOISE_COMPILED:
        text = pat.sub(" ", text)
    text = re.sub(r"\bO\b(?=\s|$)", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^[.\s]+", "", text)
    return text


def parse_options_from_raw(raw: str) -> list[dict]:
    body = clean_text(raw)
    opts: list[dict] = []
    parts = re.split(r"(?<=\s)(?=[a-d]\.\s)", body, flags=re.I)
    for p in parts:
        om = re.match(r"^([a-d])\.\s*(.+)$", p.strip(), re.I | re.S)
        if om:
            opts.append({"key": om.group(1).upper(), "text": clean_text(om.group(2))})

    # Deduplicate by key, keep longest text
    by_key: dict[str, str] = {}
    for o in opts:
        k, t = o["key"], o["text"]
        if k not in by_key or len(t) > len(by_key[k]):
            by_key[k] = t
    return [{"key": k, "text": by_key[k]} for k in sorted(by_key)]


def extract_stem(raw: str, options: list[dict]) -> str:
    body = clean_text(raw)
    first = re.search(r"\s[a-d]\.\s", body, re.I)
    stem = body[: first.start()].strip() if first else body
    return clean_text(stem)


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
        return f"Key idea ({topic}): {correct['text']}"
    return f"Key idea ({topic}): answer {answer}"


def is_promo_page(parsed: dict) -> bool:
    blob = (parsed.get("text", "") + " " + parsed.get("raw", "")).lower()
    return "comp sci" in blob and "telegram" in blob or "channel" in blob and len(parsed.get("options", [])) == 0


def build_questions() -> tuple[list[dict], list[str]]:
    pages = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    questions: list[dict] = []
    skipped: list[str] = []
    seq_id = 0

    for page in pages:
        pnum = page["page"]
        if pnum > 100:
            if is_promo_page(page.get("parsed", {})):
                skipped.append(f"page {pnum}: promo/footer (not an exam question)")
            else:
                skipped.append(f"page {pnum}: beyond question 100")
            continue

        exam_num = pnum  # one question per page 1-100
        parsed = page.get("parsed", {})
        raw = page.get("raw", "")

        if is_promo_page(parsed):
            skipped.append(f"page {pnum}: promo content")
            continue

        override = MANUAL_OVERRIDES.get(exam_num, {})
        parsed_opts = [] if override.get("options") else parse_options_from_raw(raw)
        text = override.get("text") or extract_stem(raw, parsed_opts)
        options = override.get("options") or normalize_options(parsed_opts)

        if len(text) < 12:
            skipped.append(f"page {pnum} (Q{exam_num}): stem too short after cleaning")
            continue
        if sum(1 for o in options if "(option unclear" not in o["text"]) < 2:
            skipped.append(f"page {pnum} (Q{exam_num}): fewer than 2 parseable options")
            continue

        topic = override.get("topic") or classify(text + " " + " ".join(o["text"] for o in options))
        answer = override.get("answer") or ANSWERS.get(exam_num)
        if not answer:
            skipped.append(f"page {pnum} (Q{exam_num}): missing answer key")
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
        "title": "AAU Model Exit Exam",
        "source": "Addis Ababa University (AAU) Model Exit Exam — Moodle OCR",
        "total": len(questions),
        "focusGuide": FOCUS_GUIDE,
        "questions": questions,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(questions)} questions -> {OUT_PATH}")
    if skipped:
        print(f"Skipped {len(skipped)}:")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
