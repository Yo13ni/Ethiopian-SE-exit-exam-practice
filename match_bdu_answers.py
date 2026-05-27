"""Match BDU OCR stems to known exams (2015, AAU, 2016) for answer keys."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

from bdu_parser import parse_bdu_page, is_promo

ROOT = Path(__file__).parent


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_known() -> list[dict]:
    known = []
    for path, exam_id in [
        (ROOT / "data/exams/2015/questions.json", "2015"),
        (ROOT / "data/exams/aau/questions.json", "aau"),
        (ROOT.parent.parent / "exam-app/data/exam.json", "2016"),
    ]:
        if not path.exists():
            continue
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


def match_stem(stem: str, known: list[dict], threshold: float = 0.72) -> dict | None:
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
    raw_path = ROOT / "data/exams/bdu/raw_ocr.json"
    if not raw_path.exists():
        print("Run extract_bdu_ocr.py first")
        return
    pages = json.loads(raw_path.read_text(encoding="utf-8"))
    known = load_known()
    answers: dict[int, str] = {}
    matches = []
    for page in pages:
        if is_promo(page.get("raw", "")) or page["page"] > 99:
            continue
        parsed = parse_bdu_page(page.get("raw", ""), page["page"])
        stem = parsed["text"]
        exam_num = page["page"]
        hit = match_stem(stem, known)
        if hit:
            answers[exam_num] = hit["answer"]
            matches.append((exam_num, hit["score"], hit["source"], hit["examNumber"], stem[:60]))
    out = ROOT / "data/exams/bdu/matched_answers.json"
    out.write_text(json.dumps(answers, indent=2), encoding="utf-8")
    print(f"Matched {len(answers)} answers -> {out}")
    for row in matches[:15]:
        print(f"  Q{row[0]} score={row[1]:.2f} from {row[2]}#{row[3]}: {row[4]}...")


if __name__ == "__main__":
    main()
