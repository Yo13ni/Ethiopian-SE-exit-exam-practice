"""Match 2017 OCR stems to known exams for answer keys."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "exams" / "2017" / "raw_ocr.json"
OUT_PATH = ROOT / "data" / "exams" / "2017" / "matched_answers.json"


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_known() -> list[dict]:
    known = []
    for rel in [
        "data/exams/2015/questions.json",
        "data/exams/2016/questions.json",
        "data/exams/aau/questions.json",
        "data/exams/bdu/questions.json",
        "data/exams/model1/questions.json",
        "data/exams/moe2025/questions.json",
    ]:
        path = ROOT / rel
        if not path.exists():
            continue
        exam_id = path.parent.name
        data = json.loads(path.read_text(encoding="utf-8"))
        for q in data.get("questions", []):
            known.append({
                "source": exam_id,
                "examNumber": q.get("examNumber"),
                "text": q.get("text", ""),
                "answer": q.get("answer"),
                "norm": norm(q.get("text", "")),
            })
    return known


def match_stem(stem: str, known: list[dict], threshold: float = 0.68) -> dict | None:
    n = norm(stem)
    if len(n) < 20:
        return None
    best = None
    best_score = 0.0
    for k in known:
        score = SequenceMatcher(None, n, k["norm"]).ratio()
        if score > best_score:
            best_score = score
            best = k
    if best and best_score >= threshold:
        return {**best, "score": best_score}
    return None


def main() -> None:
    if not RAW_PATH.exists():
        print("Run extract_2017_ocr.py first")
        return

    pages = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    known = load_known()
    answers: dict[int, str] = {}
    matches = []

    seen: dict[int, dict] = {}
    for page in pages:
        parsed = page.get("parsed", {})
        exam_num = parsed.get("examNumber")
        stem = parsed.get("text", "")
        if not exam_num or len(stem) < 15:
            continue
        prev = seen.get(exam_num)
        if not prev or len(stem) > len(prev.get("text", "")):
            seen[exam_num] = parsed

    for exam_num, parsed in sorted(seen.items()):
        stem = parsed.get("text", "")
        hit = match_stem(stem, known)
        if hit:
            answers[exam_num] = hit["answer"]
            matches.append((exam_num, hit["score"], hit["source"], hit["examNumber"], stem[:70]))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(answers, indent=2), encoding="utf-8")
    print(f"Matched {len(answers)} answers -> {OUT_PATH}")
    for row in matches[:20]:
        print(f"  Q{row[0]} score={row[1]:.2f} from {row[2]}#{row[3]}: {row[4]}...")


if __name__ == "__main__":
    main()
